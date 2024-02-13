from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlmodel import Session, create_engine, SQLModel

from antisocial_backend.dependencies.dependencies import get_query_token
from antisocial_backend.routes import users

app = FastAPI()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass

app = FastAPI(lifespan=app_lifespan)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app.include_router(router=users.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

