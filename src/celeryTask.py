from celery import Celery
from src.mail import create_Message, mail
from asgiref.sync import async_to_sync
from src.config import setting
c_app = Celery()

c_app = Celery(
    "worker",
    broker=setting.REDIS_URL,
    backend=setting.REDIS_URL,
)

@c_app.task()
def send_email(recipients: list[str], subject: str, html_message: str):
    message = create_Message(recipents=recipients, subject=subject, body=html_message)
    async_to_sync(mail.send_message)(message)


# The instructor told me I have to use asgiref. What is that?

# asgiref is a Python library that provides utilities for working with ASGI (Asynchronous Server Gateway Interface), which is the standard for async web servers and frameworks in Python (like FastAPI, Starlette, Django Channels).

# It includes tools like sync_to_async and async_to_sync to help run synchronous code in async contexts and vice versa.
