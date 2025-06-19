from typing import List
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import setting
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mailconfig = ConnectionConfig(
    MAIL_USERNAME=setting.MAIL_USERNAME,
    MAIL_PASSWORD=setting.MAIL_PASSWORD, # type: ignore
    MAIL_PORT=setting.MAIL_PORT,
    MAIL_FROM=setting.MAIL_FROM,
    MAIL_SERVER=setting.MAIL_SERVER,
    MAIL_FROM_NAME=setting.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR),
)  # type: ignore

mail = FastMail(config=mailconfig)  # type: ignore

# mail.send_message()
def create_Message(recipents: List[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipents, subject=subject, body=body, subtype=MessageType.html
    )  # type: ignore
    return message