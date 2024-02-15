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

@router.get("/", response_model=list[EventRead])
async def read_events(*, session:Session = Depends(get_session)):
    events = read_events_db(session=session)
    if not events:
        raise HTTPException(status_code=404, detail="Events not found")
    return events

@router.get("/{event_id}" , response_model=EventRead)
async def read_event(*, session:Session = Depends(get_session), event_id: int):
    event = read_event_db(session=session, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/", response_model=EventRead)
async def create_event(*, session:Session = Depends(get_session), event: EventCreate):  
    return create_event_db(session=session, event=event)

@router.put("/{event_id}", response_model=EventRead)
async def update_event(*, session:Session = Depends(get_session), event_id:int, event: EventUpdate):
    db_event = update_event_db(session=session, event_id=event_id, event=event)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.delete("/{event_id}")
async def delete_event(*, session:Session = Depends(get_session), event_id: int):
    if not delete_event_db(session=session, event_id=event_id):
        raise HTTPException(status_code=404, detail="Event not found")
    return {"result": "event deleted"}