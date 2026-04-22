from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pathlib import Path
from FastAPI.Ssali_Jonathan.CRUD.core.config import get_settings


BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()


mail_config = ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_FROM_NAME = settings.mail_from,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER = Path(BASE_DIR, r'D:\Training\python-frameworks-and-libraries\FastAPI\Ssali_Jonathan\CRUD\templates')
)

mail = FastMail(
    config = mail_config
)



def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients = recipients,
        subject = subject,
        body = body,
        subtype = MessageType.html
    )

    return message