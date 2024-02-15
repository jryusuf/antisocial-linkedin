import pytest
from pytest import fixture
from antisocial_backend.models.Event import *
from antisocial_backend.dependencies.database.events import *
from datetime import datetime
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.dependencies.dependencies import get_session, Session
from pydantic import ValidationError

def test_create_event_db_returns_event_object(session: Session):
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    db_event = create_event_db(session=session, event=event)
    assert db_event.type == "non-profit"
    assert db_event.name == "The Red Cross"
    assert db_event.description == "A non-profit organization"
    assert db_event.start_date != None
    assert db_event.id != None

def test_create_event_db_raises_error_on_invalid_input(session: Session):
    with pytest.raises(ValidationError):
        event = EventCreate(
            type="non-profit",
            name="The Red Cross",
            description="A non-profit organization",
            start_date="not a date")
        db_event = create_event_db(session=session, event=event)

def test_read_events_db_returns_list_of_events(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    events = read_events_db(session=session)
    assert len(events) == 2
    assert events[0].id == db_event1.id
    assert events[1].id == db_event2.id

def test_read_events_db_returns_empty_list_when_no_events(session: Session):
    events = read_events_db(session=session)
    assert len(events) == 0

def test_reads_events_db_returns_one_event(session: Session):
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    db_event = create_event_db(session=session, event=event)
    events = read_events_db(session=session)
    assert len(events) == 1
    assert events[0].id == db_event.id

def test_read_event_db_returns_event(session: Session):
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    db_event = create_event_db(session=session, event=event)
    event = read_event_db(session=session, event_id=db_event.id)
    assert event.id == db_event.id

def test_read_event_db_returns_none_when_event_not_found(session: Session):
    event = read_event_db(session=session, event_id=1)
    assert event == None

def test_read_event_db_returns_none_when_multiple_exits(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="corporation",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    event = read_event_db(session=session, event_id=1)
    assert event.type == "non-profit"
    assert event.name == "The Blue Cross"

def test_delete_event_db_deletes_event(session: Session):
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    db_event = create_event_db(session=session, event=event)
    assert delete_event_db(session=session, event_id=db_event.id) == True
    assert read_event_db(session=session, event_id=db_event.id) == None

def test_delete_event_db_returns_false_when_event_not_found(session: Session):
    assert delete_event_db(session=session, event_id=1) == False

def test_delete_event_db_returns_false_when_multiple_event_exist_with_wrong_id(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="corporation",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    assert delete_event_db(session=session, event_id=3) == False

def test_delete_event_db_deletes_and_returns_true_when_multiple_events_exist_along_with_correct_id(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="corporation",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    assert delete_event_db(session=session, event_id=db_event2.id) == True
    assert read_event_db(session=session, event_id=db_event2.id) == None

def test_update_event_db_updates_event(session: Session):
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    db_event = create_event_db(session=session, event=event)
    update_event = EventUpdate(
        type="corporation",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    updated_event = update_event_db(session=session, event_id=db_event.id, event=update_event)
    assert updated_event.id == db_event.id
    assert updated_event.type == "corporation"
    assert updated_event.name == "The Blue Cross"
    assert updated_event.description == "A non-profit organization"

def test_update_event_db_returns_none_when_event_not_found(session: Session):
    update_event = EventUpdate(
        type="corporation",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    updated_event = update_event_db(session=session, event_id=1, event=update_event)
    assert updated_event == None

def test_update_event_db_returns_none_when_multiple_events_exist_with_wrong_id(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="corporation",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    update_event = EventUpdate(
        type="corporation",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    updated_event = update_event_db(session=session, event_id=3, event=update_event)
    assert updated_event == None

def test_update_event_db_returns_updated_event_when_multiple_events_exits(session: Session):
    event1 = EventCreate(
        type="non-profit",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    event2 = EventCreate(
        type="charity",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    db_event1 = create_event_db(session=session, event=event1)
    db_event2 = create_event_db(session=session, event=event2)
    update_event = EventUpdate(
        type="corporation",
        name="The Blue Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    updated_event = update_event_db(session=session, event_id=1, event=update_event)
    assert updated_event.id == db_event1.id
    assert updated_event.type == "corporation"
    assert updated_event.name == "The Blue Cross"
    assert updated_event.description == "A non-profit organization"
    assert updated_event.start_date != None