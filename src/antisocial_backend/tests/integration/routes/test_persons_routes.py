from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead
from antisocial_backend.models.Person import PersonCreate, Person, PersonRead, PersonUpdate
from antisocial_backend.dependencies.database.persons import *

def test_read_persons_return_404_when_there_is_no_person(session: Session, client: TestClient):
    response = client.get("/persons")
    assert response.status_code == 404
    assert response.json() == {"detail": "Person not found"}

def test_read_persons_return_persons(session: Session, client: TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.get("/persons")
    assert response.status_code == 200

    data = response.json()

    assert data[0]["firstname"] == "John"
    assert data[0]["lastname"] == "Doe"
    assert data[0]["is_in_contact"] == False
    assert data[0]["id"] == 1
    assert data[0]["date_of_birth"] == None

def test_read_persons_return_two_person_when_two_exits(session:Session, client:TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    person = PersonCreate(firstname="Jane", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.get("/persons")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["firstname"] == "John"
    assert data[1]["firstname"] == "Jane"

def test_read_person_return_404_when_person_not_found(session: Session, client: TestClient):
    response = client.get("/persons/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Person not found"}

def test_read_person_return_person(session: Session, client: TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.get("/persons/1")
    assert response.status_code == 200

    data = response.json()
    assert data["firstname"] == "John"
    assert data["lastname"] == "Doe"
    assert data["is_in_contact"] == False
    assert data["id"] == 1
    assert data["date_of_birth"] == None

def test_read_person_returns_correct_person_when_multiple_persons_exits_in_db(session:Session, client: TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    person = PersonCreate(firstname="Jane", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.get("/persons/2")
    assert response.status_code == 200

    data = response.json()
    assert data["firstname"] == "Jane"
    assert data["lastname"] == "Doe"
    assert data["is_in_contact"] == False
    assert data["id"] == 2
    assert data["date_of_birth"] == None

def test_create_person_returns_person(session: Session, client: TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    response = client.post("/persons/", json=person.model_dump())
    assert response.status_code == 200

    data = response.json()
    assert data["firstname"] == "John"
    assert data["lastname"] == "Doe"
    assert data["is_in_contact"] == False
    assert data["id"] == 1
    assert data["date_of_birth"] == None

def test_create_return_422_when_given_invalid_input(session: Session, client: TestClient):
    response = client.post("/persons/", json={
        "firstname": "John"
    })
    assert response.status_code == 422

def test_delete_person_returns_404_when_person_not_found(session: Session, client: TestClient):
    response = client.delete("/persons/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Person not found"}

def test_delete_person_deletes_person_and_returns_200_when_user_exist(session: Session, client: TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.delete("/persons/1")
    assert response.status_code == 200
    assert response.json() == {"result": "person deleted"}

def test_delete_person_delete_correct_person_when_multiple_exits(session:Session, client:TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    person = PersonCreate(firstname="Jane", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.delete("/persons/2")
    assert response.status_code == 200
    assert response.json() == {"result": "person deleted"}

    response = client.get("/persons")
    data = response.json()
    assert len(data) == 1
    assert data[0]["firstname"] == "John"

def test_update_person_returns_404_when_person_not_found(session: Session, client: TestClient):
    person = PersonUpdate(firstname="John")
    response = client.put("/persons/1", json=person.model_dump())
    assert response.status_code == 404
    assert response.json() == {"detail": "Person not found"}

def test_update_person_return_updated_person_when_person_exits(session:Session, client:TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)

    response = client.put("/persons/1", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "date_of_birth": "1990-01-01",
        "is_in_contact": True
    })
    assert response.status_code == 200

    data = response.json()
    assert data["firstname"] == "Jane"
    assert data["lastname"] == "Doe"
    assert data["is_in_contact"] == True
    assert data["id"] == 1

@pytest.mark.skip
def test_update_person_return_422_when_given_invalid_input(session:Session, client:TestClient):
    person = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person)
    response = client.put("/persons/1", json={})
    assert response.status_code == 422

def test_update_person_update_correct_person_when_multiple_exits(session:Session, client:TestClient):
    person1 = PersonCreate(firstname="John", lastname="Doe")
    create_person_db(session=session, person=person1)
    person2 = PersonCreate(firstname="Jane", lastname="Doe")
    create_person_db(session=session, person=person2)

    response = client.put("/persons/2", json={
        "firstname": "Diane",
        "lastname": "Doe",})
    assert response.status_code == 200
    person1_response = client.get("/persons/1")
    assert person1_response.status_code == 200
    person1_data = person1_response.json()
    assert person1_data["firstname"] == "John"
    assert person1_data["lastname"] == "Doe"

    person2_response = client.get("/persons/2")
    assert person2_response.status_code == 200
    person2_data = person2_response.json()
    assert person2_data["firstname"] == "Diane"
    assert person2_data["lastname"] == "Doe"

