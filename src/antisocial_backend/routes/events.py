from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.models.User import UserCreate, User,UserRead, UserUpdate
from antisocial_backend.dependencies.dependencies import get_session, Session
from antisocial_backend.dependencies.database.events import *


router = APIRouter(
    prefix="/events",
    tags=["events"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


class Event():
    session = Session = Depends(get_session)
    
    @router.get("/", response_model=list[EventRead])
    async def read_events(self):
        events = read_events_db(session=self.session)
        if not events:
            raise HTTPException(status_code=404, detail="Events not found")
        return events

    @router.get("/{event_id}" , response_model=EventRead)
    async def read_event(self, event_id: int):
        event = read_event_db(session=self.session, event_id=event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    @router.post("/", response_model=EventRead)
    async def create_event(self, event: EventCreate):  
        return create_event_db(session=self.session, event=event)

    @router.put("/{event_id}", response_model=EventRead)
    async def update_event(self, event_id:int, event: EventUpdate):
        db_event = update_event_db(session=self.session, event_id=event_id, event=event)
        if not db_event:
            raise HTTPException(status_code=404, detail="Event not found")
        return db_event

    @router.delete("/{event_id}")
    async def delete_event(self, event_id: int):
        if not delete_event_db(session=self.session, event_id=event_id):
            raise HTTPException(status_code=404, detail="Event not found")
        return {"result": "event deleted"}
    
event = Event()