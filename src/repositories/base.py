from sqlalchemy import select, insert, update, delete as sa_delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data):
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit(self, data, **filter_by):
        stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(stmt)

    async def delete(self, **filter_by):
        stmt = sa_delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
