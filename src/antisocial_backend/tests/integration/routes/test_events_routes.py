from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead
from antisocial_backend.models.Person import PersonCreate, Person, PersonRead, PersonUpdate
from antisocial_backend.dependencies.database.events import *
from datetime import datetime

def test_read_events_return_404_when_there_is_no_event(session: Session, client: TestClient):
    response = client.get("/events")
    assert response.status_code == 404
    assert response.json() == {"detail": "Events not found"}

def test_read_events_return_events(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    response = client.get("/events")
    assert response.status_code == 200

    data = response.json()

    assert data[0]["name"] == "The Red Cross"
    assert data[0]["start_date"] != None
    assert data[0]["id"] == 1

def test_read_events_return_multiple_events_when_exits(session:Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    event = EventCreate(name="The Blue Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    response = client.get("/events")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "The Red Cross"
    assert data[1]["name"] == "The Blue Cross"

def test_read_event_return_404_when_event_not_found(session: Session, client: TestClient):
    response = client.get("/events/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_read_event_return_event(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    event_db = create_event_db(session=session, event=event)

    response = client.get("/events/1")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 1

def test_read_event_returns_correct_event_when_multiple_exits(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    event = EventCreate(name="The Blue Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    response = client.get("/events/2")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "The Blue Cross"
    assert data["start_date"] != None
    assert data["id"] == 2

def test_delete_events_return_404_when_event_not_found(session: Session, client: TestClient):
    response = client.delete("/events/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_delete_event_delete_event(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    event_db = create_event_db(session=session, event=event)

    response = client.delete("/events/1")
    assert response.status_code == 200
    assert response.json() == {"result": "event deleted"}

    response = client.get("/events/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_delete_event_delete_correct_event_when_multiple_exits(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    event = EventCreate(name="The Blue Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    response = client.delete("/events/2")
    assert response.status_code == 200
    assert response.json() == {"result": "event deleted"}

    response = client.get("/events/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_create_event_returns_event(session: Session, client: TestClient):
    response = client.post("/events", json={
        "name": "The Red Cross",
        "type": "non-profit",
        "description": "A non-profit organization",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 1

def test_create_event_returns_422_when_start_date_is_not_a_date(session: Session, client: TestClient):
    response = client.post("/events", json={
        "name": "The Red Cross",
        "type": "non-profit",
        "description": "A non-profit organization",
        "start_date": "not a date"
    })
    assert response.status_code == 422

def test_update_event_returns_422_when_input_is_invalid(session: Session, client: TestClient):
    response = client.put("/events/1", json={
        "name": "The Red Cross",
        "type": "non-profit",
        "description": "A non-profit organization",
        "start_date": "not a date"
    })
    assert response.status_code == 422

def test_update_returns_404_when_event_not_found(session: Session, client: TestClient):
    response = client.put("/events/1", json={
        "name": "The Red Cross",
        "type": "non-profit",
        "description": "A non-profit organization",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Event not found"}

def test_update_returns_updated_event_when_exists(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    event_db = create_event_db(session=session, event=event)

    response = client.put("/events/1", json={
        "name": "The Blue Cross",
        "type": "demo",
        "description": "desc",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "The Blue Cross"
    assert data["start_date"] != None
    assert data["id"] == 1
    assert data["type"] == "demo"

def test_update_returns_updated_event_when_multiple_events_exists(session: Session, client: TestClient):
    event = EventCreate(name="The Red Cross",type="demo",description="desc",start_date=datetime.now())
    create_event_db(session=session, event=event)

    event = EventCreate(name="The Blue Cross",type="demo",description="desc",start_date=datetime.now())
    event_db = create_event_db(session=session, event=event)

    response = client.put("/events/2", json={
        "name": "The Green Cross",
        "type": "demo",
        "description": "desc",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "The Green Cross"
    assert data["start_date"] != None
    assert data["id"] == 2
    assert data["type"] == "demo"

    event_2_from_db = read_event_db(session=session, event_id=2)
    assert event_2_from_db.name == "The Green Cross"