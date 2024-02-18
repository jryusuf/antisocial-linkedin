import contextlib
from typing import Any, AsyncIterator

from antisocial_backend.resources.notes.settings import settings
from sqlalchemy.ext.asyncio import(
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    async_session,
    
)
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class DatabaseSessionManager:
    def __init__(self, host:str, engine_kwargs: dict[str, Any]= {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._session_maker = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._session_maker = None


    @contextlib.asynccontextmanager
    async def connect(self)->AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        async with self._session_maker() as session:
            try:
                yield session
            except Exception:
                session.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self)-> AsyncIterator[AsyncSession]:
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        
        session = self._session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

sessionmanager = DatabaseSessionManager(settings.database_url, {"echo":settings.echo_sql})

async def get_db_session():
    async with sessionmanager.connect() as session:
        yield session