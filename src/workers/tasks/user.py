from celery import shared_task
from sqlalchemy import select, update

from src.core.config import settings
from src.core.logger import logger
from src.core.role import Role
from src.db.database import get_sync_db_session
from src.domain.models import User
from src.workers.tasks import send_ban_notification, send_moderator_notification


@shared_task
def check_to_ban():
    with get_sync_db_session() as session:
        try:
            stmt = select(User).where(
                User.reputation < settings.BAN_THRESHOLD, User.is_banned == False
            )

            users_to_ban = session.execute(stmt).scalars().all()

            if users_to_ban:
                logger.info(f"Celery worker detected {len(users_to_ban)} users to ban")

                stmt_update = (
                    update(User)
                    .where(User.id.in_([user.id for user in users_to_ban]))
                    .values(is_banned=True)
                )

                session.execute(stmt_update)
                session.commit()

                for user in users_to_ban:
                    send_ban_notification.apply_async(
                        args=[user.email], queue="notification"
                    )

                return len(users_to_ban)
        except Exception as e:
            logger.error(str(e))
            session.rollback()
            raise
        finally:
            session.close()


@shared_task
def check_to_make_moderator():
    with get_sync_db_session() as session:
        try:
            stmt = select(User).where(
                User.reputation > settings.MODERATOR_THRESHOLD, User.role == Role.USER
            )

            users_to_make_moderator = session.execute(stmt).scalars().all()

            if users_to_make_moderator:
                logger.info(
                    f"Celery worker detected {len(users_to_make_moderator)} users to make moderator"
                )
                stmt_update = (
                    update(User)
                    .where(User.id.in_([user.id for user in users_to_make_moderator]))
                    .values(role=Role.MODERATOR)
                )

                session.execute(stmt_update)
                session.commit()

                for user in users_to_make_moderator:
                    send_moderator_notification.apply_async(
                        args=[user.email], queue="notification"
                    )

                return len(users_to_make_moderator)
        except Exception as e:
            logger.error(str(e))
            session.rollback()
            raise
        finally:
            session.close()
