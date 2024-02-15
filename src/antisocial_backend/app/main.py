from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from antisocial_backend.dependencies.dependencies import get_query_token
from antisocial_backend.routes import users
from antisocial_backend.routes import persons
from antisocial_backend.routes import organizations
from antisocial_backend.routes import events
from antisocial_backend.dependencies.dependencies import create_db_and_tables

app = FastAPI()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass  

app = FastAPI(lifespan=app_lifespan)

app.include_router(router=users.router)
app.include_router(router=persons.router)
app.include_router(router=organizations.router)
app.include_router(router=events.router)
@app.get("/")
async def read_root():
    return {"Hello": "World"}

