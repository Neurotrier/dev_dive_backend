from datetime import timedelta

from celery import Celery

from src.core.config import settings

celery_app = Celery("celery", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.beat_schedule = {
    "check_to_ban": {
        "task": "src.workers.tasks.user.check_to_ban",
        "schedule": timedelta(seconds=30),
    },
    "check_to_make_moderator": {
        "task": "src.workers.tasks.user.check_to_make_moderator",
        "schedule": timedelta(seconds=30),
    },
}

celery_app.autodiscover_tasks(
    ["src.workers.tasks.user", "src.workers.tasks.notification"]
)
