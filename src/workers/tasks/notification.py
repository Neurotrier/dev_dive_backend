from celery import shared_task

from src.core.logger import logger


@shared_task(queue="notification")
def send_ban_notification(email):
    # stub
    logger.info(
        f"Dear {email}, you account has been banned due to your low reputation level on the platform"
    )


@shared_task(queue="notification")
def send_moderator_notification(email):
    # stub
    logger.info(
        f"Dear {email}, you account has been promoted to the moderator due to your high reputation level on the platform"
    )
