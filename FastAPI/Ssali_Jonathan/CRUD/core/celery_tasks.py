from celery import Celery
from asgiref.sync import async_to_sync

from FastAPI.Ssali_Jonathan.CRUD.core.mail import create_message, mail


c_app = Celery()

c_app.config_from_object('FastAPI.Ssali_Jonathan.CRUD.core.config')


@c_app.task()
def send_email(recipients: list[str], subject: str, body: str):

    message = create_message(
        recipients = recipients,
        subject = subject,
        body = body
    )
    
    async_to_sync(mail.send_message)(message)

    print("Email Sent...")

