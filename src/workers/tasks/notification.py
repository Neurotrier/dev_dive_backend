import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from celery import shared_task

from src.core.config import settings
from src.core.logger import logger


@shared_task(queue="notification")
def send_ban_notification(email):
    subject = "Dev Dive"
    body = f"Dear {email}, you account has been banned due to your low reputation level on the platform"

    message = MIMEMultipart()
    message["From"] = formataddr(
        (str(Header("no_reply@example.com", "utf-8")), "no_reply@example.com")
    )
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.APP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        logger.info(f"Could not ban {email} due to {str(e)}")


@shared_task(queue="notification")
def send_moderator_notification(email):
    subject = "Dev Dive"
    body = f"Dear {email}, you account has been promoted to the moderator due to your high reputation level on the platform"

    message = MIMEMultipart()
    message["From"] = formataddr(
        (str(Header("no_reply@example.com", "utf-8")), "no_reply@example.com")
    )
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.APP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        logger.info(f"Could not promote {email} due to {str(e)}")
