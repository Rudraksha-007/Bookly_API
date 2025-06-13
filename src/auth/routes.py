from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserBooksModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserModel, UserLoginModel
from .utils import create_access_token, decode_token, verify_Passw
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_jti_to_blocklist
from .dependencies import get_curr_user, RoleChecker
from src.errors import *

auth_router = APIRouter()
user_service = UserService()
role_service = RoleChecker(["admin", "user"])


REFRESH_TOKEN_EXPIRY = 2


# Bearer Token
@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    newusr = await user_service.create_user(user_data, session)
    return newusr


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password
    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_Passw(password, user.password_hash)  # type:ignore
        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,  # type:ignore
                    "user_id": str(user.uid),
                    # type:ignore,
                    "role": user.role,
                }
            )
            refresh_token = create_access_token(
                user_data={
                    "email": user.email,  # type:ignore
                    "user_id": str(user.uid),
                    # type:ignore
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )
            return JSONResponse(
                content={
                    "message": "login succesfull",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
    else:
        raise InvalidEmail_Or_Password()

@auth_router.get("/refresh_token")
async def renew_session(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_accessToken = create_access_token(user_data=token_details["user"])
        return JSONResponse(content={"access_token": new_accessToken})
    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_curr_user), _: bool = Depends(role_service)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    JTI = token_details["jti"]
    if await add_jti_to_blocklist(JTI):
        return JSONResponse(
            content={"message": "Logged Out succesfully"},
            status_code=status.HTTP_200_OK,
        )
    else:
        raise LogoutFailed()
