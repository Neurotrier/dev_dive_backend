from typing import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL, pool_recycle=3600, pool_pre_ping=True, echo=settings.DEBUG
)
factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
