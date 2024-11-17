from contextlib import contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from src.core.config import settings

async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)
async_factory = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,
)
sync_factory = sessionmaker(sync_engine, expire_on_commit=False, class_=Session)


@contextmanager
def get_sync_db_session() -> Generator[Session, None, None]:
    with sync_factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()
