from fastapi import FastAPI, Request
from antisocial_backend.resources.notes.note_model import notes
from antisocial_backend.resources.events.event_model import events
from antisocial_backend.resources.contacts.contact_model import contacts
from antisocial_backend.resources.roadmaps.roadmaps_model import roadmaps
from antisocial_backend.resources.notes.database_session import sessionmanager
from antisocial_backend.resources.notes.settings import settings
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
import logging 
import json
from antisocial_backend.resources.notes.loggin_lib import RouterLoggingMiddleware
from antisocial_backend.resources.notes.logger import logger


async def create_db_and_tables():
    async with sessionmanager._engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
 
 

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await create_db_and_tables()
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
    
app = FastAPI(
    servers=[{"url": "http://localhost:8000", 
              "description": "Localhost"},{
                    "url": "https://localhost/events:8000",
                    "description": "Events"
              }],

    
    lifespan=app_lifespan, 
    title = "Antisocial Networking", 
    description = "A simple social network", 
    version = "0.1.0")

app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__))

""" @app.middleware("http")
async def log_middleware(request: Request, call_next):

    body = await request.body()
    body.decode("utf-8").replace("'", '"')   

    response = await call_next(request)

    log_dict =  {
        "url": request.url.path,
        "request": json.loads(body) if body else None,
        "method": request.method,
        "client": request.client.host,
        #"user-agent": (request.headers.get("user-agent")),
        "response_code": response.status_code,
    }
    logger.info(log_dict)
    return response  """

@app.get("/", response_model=list[notes.Read])
async def read_root():
    return await notes.list()

@app.get("/{id}", response_model = notes.Read)
async def read_note(id: int):
    return await notes.get(id)


@app.post("/", response_model = notes.Read)
async def create_note(note: notes.Create):
    return await notes.create(note)


@app.delete("/{id}")
async def delete_note(id: int):
    result = await notes.delete(id)
    return {"success": result}

@app.put("/{id}", response_model = notes.Read)
async def update_note(id: int, note: notes.Update):
    return await notes.update(id, note)

subapi = FastAPI(lifespan=app_lifespan)

@subapi.post("/", response_model = events.Read)
async def create_event(event: events.Create):
    return await events.create(event)

app.mount("/events", subapi, name="events")


subapi2 = FastAPI(lifespan=app_lifespan)

@subapi2.post("/", response_model = contacts.Read)
async def create_contact(contact: contacts.Create):
    return await contacts.create(contact)

app.mount("/contacts", subapi2, name="contacts")

subapi3 = FastAPI(lifespan=app_lifespan)

@subapi3.post("/", response_model = roadmaps.Read)
async def create_roadmap(roadmap: roadmaps.Create):
    return await roadmaps.create(roadmap)

app.mount("/roadmaps", subapi3, name="roadmaps")



app_hello = FastAPI(lifespan=app_lifespan)

@app_hello.post("/")
async def hello_world():
    return {"message": "Hello World"}

""" app_hello.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__)) """