from fastapi import FastAPI, Depends

from antisocial_backend.dependencies.dependencies import get_query_token
from antisocial_backend.routes import users

app = FastAPI()

app.include_router(router=users.router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

