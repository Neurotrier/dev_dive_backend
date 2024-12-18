from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_async_db_session

DBSession = Annotated[AsyncSession, Depends(get_async_db_session)]
