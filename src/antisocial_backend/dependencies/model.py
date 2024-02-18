from sqlmodel import Field
from pydantic import create_model
from abc import ABC, abstractmethod
#from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import Depends
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine 
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from fastapi import HTTPException

engine = create_async_engine("sqlite+aiosqlite:///test2.db", echo=False)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Model(ABC):
    def __init__(self, base_model, table_name:str):
        self.Base = base_model
        self.Create = create_model(
            __model_name = f"{table_name}Create",
              __base__=self.Base)
        self.Read = create_model(
            __model_name = f"{table_name}Read",
              __base__=self.Base,id=(int,...))
        self.Update = create_model(
            __model_name = f"{table_name}Update",
              __base__=self.Base)
        self.Delete = create_model(
            __model_name = f"{table_name}Delete",
              __base__=self.Base)
        self.Table = create_model(
            table_name,
              __base__=self.Base,
              id= (int,
                   Field(primary_key=True,
                         default=None)),
              __cls_kwargs__={"table":True}
        )
        self.create = self.create
        self.get = self.get
        self.list = self.list
        self.delete = self.delete
        self.update = self.update

    async def find(self, id:int):
        async with SessionLocal() as session:
            result = await session.get(self.Table, id)
            if result is None:
                raise HTTPException(status_code=404, detail="Note not found")
            return result
        
    async def create(self, data):
        async with SessionLocal() as session:
            db_data = self.Table.model_validate(data)
            session.add(db_data)
            await session.commit()
            await session.refresh(db_data)
            return db_data
        
    async def get(self, id:int):
        async with SessionLocal() as session:
            return await self.find(id)
          
    async def list(self):
        async with SessionLocal() as session:
            q = select(self.Table)
            results =  await session.execute(q)
            return results.scalars().all()
        
    async def delete(self, id: int):
        async with SessionLocal() as session:
            db_data = await self.find(id)
            if not db_data:
                return False
            await session.delete(db_data)
            await session.commit()
            return True
        
    async def update(self, id:int, data):
        async with SessionLocal() as session:
            db_data = await self.find(id)
            if not db_data:
                return None
            data = data.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(db_data, key, value)
            session.add(db_data)
            await session.commit()
            await session.refresh(db_data)
            return db_data



