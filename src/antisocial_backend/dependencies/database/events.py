from antisocial_backend.models.Event import *
from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

def create_event_db(*, session: Session, event: EventCreate)-> EventRead:
    db_event = Event.model_validate(event)
    session.add(db_event)
    session.commit()
    session.refresh(db_event)
    return db_event

def read_events_db(*, session: Session)-> list[EventRead]:
    return session.exec(select(Event)).all()

def read_event_db(*, session: Session, event_id: int)-> EventRead:
    return session.get(Event, event_id)

def delete_event_db(*, session: Session, event_id: int)-> bool:
    event_db = session.get(Event, event_id)
    if not event_db:
        return False
    session.delete(event_db)
    session.commit()
    return True

def update_event_db(*, session: Session, event_id: int, event: EventUpdate)-> EventRead:
    event_db = session.get(Event, event_id)
    if not event_db:
        return None
    event_data = event.model_dump(exclude_unset=True)
    for key, value in event_data.items():
        setattr(event_db, key, value)
    session.add(event_db)
    session.commit()
    session.refresh(event_db)
    return event_db
    