from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import Any, List
from src.db.models import User


user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        print("init.")
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        print("Token Bearer: __call__ was called")
        creds = await super().__call__(request)
        token = creds.credentials  # type:ignore

        token_data = decode_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "" "error": "Invalid/Expired token",
                    "resolution": "Get a new token",
                },
            )
        JTI = token_data["jti"]
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "" "error": "Invalid/Expired token",
                    "resolution": "Get a new token",
                },
            )

        print(JTI)
        if await token_in_blocklist(JTI):  # type:ignore
            print("Toke is in the Block list!")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token has been revoked or invalid.",
                    "resolution": "Get a new token",
                },
            )

        self.verify_token_data(token_data)
        return token_data  # type:ignore

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method.")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:

        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token",
            )


async def get_curr_user(
    toke_data: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    userEmail = toke_data["user"]["email"]
    user = await user_service.get_user_by_email(userEmail, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_User: User = Depends(get_curr_user)) -> Any:
        if current_User.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user.",
            )
        return True
