from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic, List, Optional
from src.models.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> ModelType:
        item = self.model(**kwargs)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        item = await self.get(id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            await self.session.commit()
            await self.session.refresh(item)
        return item

    async def delete(self, id: int) -> bool:
        item = await self.get(id)
        if item:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False
