from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
import uuid
from src.config import setting
import logging
from itsdangerous import URLSafeTimedSerializer

passwd_context = CryptContext(schemes=["bcrypt"])


ACCESS_TOKEN_EXPIRY = 3600


def generate_phash(password: str) -> str:  # type:ignore
    hash = passwd_context.hash(password)
    return hash


def verify_Passw(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False # type: ignore
):  # type:ignore

    payload = {}
    payload["user"] = user_data
    expire_time = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["exp"] = int(expire_time.timestamp())
    payload["jti"] = str(uuid.uuid4)
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=setting.JWT_SECRET, algorithm=setting.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:  # type:ignore
    try:
        token_data = jwt.decode(
            jwt=token, key=setting.JWT_SECRET, algorithms=[setting.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as error:
        logging.exception(error)
        return None  # type:ignore


serializer = URLSafeTimedSerializer(secret_key=setting.JWT_SECRET,salt="email-configuration")
def createURL_safe_Token(data: dict):
    token=serializer.dumps(data)
    return token

def decode_URL_safeToken(token:str):
    try:
        token_data=serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))
