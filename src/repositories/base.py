from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model = model_cls

    async def get_by_pk(self, **filter_by) -> Optional[T]:
        query = select(self._model).filter_by(**filter_by)
        res = await self._session.execute(query)
        first_result = res.first()
        return first_result[0] if first_result else None

    async def get_all(self) -> List[T]:
        query = select(self._model)
        res = await self._session.execute(query)
        return [row[0] for row in res.all()]

    async def get_by_filter(self, **filter_by) -> List[T]:
        query = select(self._model).filter_by(**filter_by).distinct()
        res = await self._session.execute(query)
        return [row[0] for row in res.all()]

    async def add(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def add_all(self, records: List[T]) -> List[T]:
        self._session.add_all(records)
        await self._session.flush()
        for record in records:
            await self._session.refresh(record)
        return records

    async def update(self, data: dict, **filter_by) -> Optional[T]:
        record = await self.get_by_pk(**filter_by)
        if record is not None:
            filtered_data = {k: v for k, v in data.items() if v is not None}

            update_query = (
                update(self._model).values(**filtered_data).filter_by(**filter_by)
            )
            await self._session.execute(update_query)

            select_query = select(self._model).filter_by(**filter_by)
            res = await self._session.execute(select_query)
            first_result = res.first()
            return first_result[0] if first_result else None

    async def delete(self, **filter_by) -> Optional[int]:
        record = await self.get_by_pk(**filter_by)
        if record is not None:
            query = delete(self._model).filter_by(**filter_by)
            await self._session.execute(query)
            return record.id

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
