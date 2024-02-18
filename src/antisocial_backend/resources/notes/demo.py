import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field

from basesqlmodel import Base

engine = create_async_engine("sqlite+aiosqlite:///test.db")
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Potato(Base, table=True):
    id: int = Field(primary_key=True)
    name: str


async def main():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Interact with the Potato table
    async with SessionLocal() as session:
        obj = await Potato.create(session, name="Potato")
        print(f"Potato created: {repr(obj)}")

        obj = await Potato.get(session, name="Potato")
        print(f"Potato retrieved: {repr(obj)}")

        await obj.update(session, name="Fake Potato")
        print(f"Potato updated: {repr(obj)}")

        """ await Potato.delete(session, name="Fake Potato")
        print(f"Potato deleted: {repr(obj)}") """

        objs = await Potato.get_multi(session)
        print(f"Confirm that the database is empty: {objs}")


asyncio.run(main())