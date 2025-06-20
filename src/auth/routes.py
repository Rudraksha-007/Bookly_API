from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .utils import generate_phash
from .schemas import (
    UserCreateModel,
    UserBooksModel,
    PasswordResetReqModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserModel, UserLoginModel, EmailModel
from .utils import (
    create_access_token,
    decode_token,
    verify_Passw,
    createURL_safe_Token,
    decode_URL_safeToken,
)
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_jti_to_blocklist
from .dependencies import get_curr_user, RoleChecker
from src.errors import *
from src.mail import create_Message, mail
from src.config import setting

# from utils import create_access_token

auth_router = APIRouter()
user_service = UserService()
role_service = RoleChecker(["admin", "user"])


REFRESH_TOKEN_EXPIRY = 2


# Bearer Token


@auth_router.post("/sendMail")
async def send_mail(mailaddr: EmailModel):
    emails = mailaddr.addresses
    html = "<h1>Welcome to Bookly.</h1>"
    message = create_Message(recipents=emails, subject="Welcome Email", body=html)
    await mail.send_message(message)  # type: ignore
    return {"message": "Email sent please check your inbox."}


@auth_router.post("/signup", response_model=Any, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
    response_model=None,
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    newusr = await user_service.create_user(user_data, session)

    token = createURL_safe_Token({"email": email})

    link = f"http://{setting.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your email</h1>
    <p>Please click <a href="{link}">this</a> link to verify your email.</p>
    """

    message = create_Message(
        recipents=[email], subject="Verification email", body=html_message
    )

    await mail.send_message(message)  # type: ignore

    return {
        "Message": "Account Created! Please check your email to verify your account.",
        "user": newusr,
    }


@auth_router.get("/verify/{token}", response_model=None)
async def verifyUserAccounts(token: str, session: AsyncSession = Depends(get_session)):
    toke_data = decode_URL_safeToken(token)
    email = toke_data.get("email")  # type: ignore
    if email:
        user = await user_service.get_user_by_email(email, session)
        if not user:
            raise UnableToFetchResource()
        await user_service.update_user(user, {"is_verified": True}, session)  # type: ignore

        return JSONResponse(
            content={"message": "Account was verified succesfully."},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "Account was not verified."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetReqModel):
    email = email_data.email

    token = createURL_safe_Token({"email": email})

    link = f"http://{setting.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click <a href="{link}">this</a> link to reset your password.</p>
    """

    message = create_Message(
        recipents=[email], subject="Verification email", body=html_message
    )

    await mail.send_message(message)  # type: ignore

    return JSONResponse(
        content={
            "Message": "Please check your email for instructions to reset your password"
        },
        status_code=status.HTTP_200_OK,
    )  # type: ignore


@auth_router.post("/password-reset-confirm/{token}")
async def reset_Account_password(
    token: str,
    password: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    new_password=password.new_password
    
    if  new_password!= password.confirm_password:
        raise HTTPException(detail="Passwords donot match",status_code=status.HTTP_400_BAD_REQUEST)
    

    toke_data = decode_URL_safeToken(token)

    email = toke_data.get("email")  # type: ignore

    if email:
        user = await user_service.get_user_by_email(email, session)

        if not user:
            raise UnableToFetchResource()

        passwordHash=generate_phash(new_password)
        await user_service.update_user(
            user, {"password_hash":passwordHash },session
        )  # type: ignore

        return JSONResponse(
            content={"message": "Password Updated successfully"},
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content={"message": "An error occured"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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
