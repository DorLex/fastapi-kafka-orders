import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail

from src.config import DOTENV_PATH

load_dotenv(DOTENV_PATH)

mail_connection_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_USERNAME'),
    MAIL_FROM_NAME=os.getenv('MAIL_FROM_NAME'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fast_mail = FastMail(mail_connection_conf)
