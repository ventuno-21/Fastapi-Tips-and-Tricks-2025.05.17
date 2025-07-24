from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseService:
    def __init__(self, model: SQLModel, session: AsyncSession):
        self.model = model
        self.session = session

    async def _get(self, id: UUID):
        return await self.session.get(self.model, id)

    async def _add(self, entity: SQLModel):
        print("*** inside base service/_add ***")
        print("*** inside base service/_add/model =  ***", entity)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity: SQLModel):
        return await self._add(entity)

    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)
        await self.session.commit()
