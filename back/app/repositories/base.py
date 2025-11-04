from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, **filters) -> Optional[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def exists_by_name(self, name: str) -> bool:
        """Check if a post with the given name already exists."""
        result = await self.session.execute(
            select(self.model.id).where(self.model.name == name)
        )
        return result.scalar_one_or_none() is not None

    async def list(self, offset: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj_in) -> ModelType:
        obj = self.model(**obj_in) if isinstance(obj_in,
                                                 dict) else self.model(**obj_in.dict())
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update(self, db_obj: ModelType, update_data: dict) -> ModelType:
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()
