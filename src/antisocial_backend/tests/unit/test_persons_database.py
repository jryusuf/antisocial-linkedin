import pytest
from sqlmodel import Session, select
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.Person import PersonCreate, Person, PersonRead, PersonUpdate
from antisocial_backend.dependencies.database.persons import *

def test_create_erson_db_creates_person(session: Session):
    person = PersonCreate(firstname="John", lastname="Doe")
    person_db = create_person_db(session=session, person=person)

    person_from_db = session.get_one(Person, person_db.id)
    assert person_from_db.firstname == "John"
    assert person_from_db.lastname == "Doe"
    assert person_from_db.date_of_birth == None
    assert person_from_db.is_in_contact == False

def test_read_persons_db_returns_list_of_persons(session: Session):
    person1 = PersonCreate(firstname="John", lastname="Doe")
    person2 = PersonCreate(firstname="Jane", lastname="Doe")
    person_db1 = create_person_db(session=session, person=person1)
    person_db2 = create_person_db(session=session, person=person2)

    persons = read_persons_db(session=session)
    assert len(persons) == 2
    assert persons[0].firstname == "John"
    assert persons[1].firstname == "Jane"

def test_read_persons_db_returns_empty_list(session: Session):
    persons = read_persons_db(session=session)
    assert len(persons) == 0

def test_read_person_db_returns_person(session: Session):
    person = PersonCreate(firstname="John", lastname="Doe")
    person_db = create_person_db(session=session, person=person)

    person_from_db = read_person_db(session=session, person_id=person_db.id)
    assert person_from_db.firstname == "John"
    assert person_from_db.lastname == "Doe"
    assert person_from_db.date_of_birth == None
    assert person_from_db.is_in_contact == False

def test_read_person_db_returns_none_with_invalid_id(session: Session):
    person_from_db = read_person_db(session=session, person_id=1)
    assert person_from_db == None

def test_delete_person_db_deletes_person(session: Session):
    person = PersonCreate(firstname="John", lastname="Doe")
    person_db = create_person_db(session=session, person=person)
    persons_from_db = read_persons_db(session=session)
    assert len(persons_from_db) == 1

    delete_person_db(session=session, person_id=person_db.id)
    persons_from_db = read_persons_db(session=session)
    assert len(persons_from_db) == 0

def test_delete_person_db_returns_false_when_user_not_found(session: Session):
    result = delete_person_db(session=session, person_id=1)
    assert result == False

def test_delete_person_db_returns_true_when_user_found_and_deleted(session: Session):
    person = PersonCreate(firstname="John", lastname="Doe")
    person_db = create_person_db(session=session, person=person)
    result = delete_person_db(session=session, person_id=person_db.id)
    assert result == True

def test_delete_person_db_deletes_correct_person_when_valid_id(session:Session):
    person1 = PersonCreate(firstname="John", lastname="Doe")
    person2 = PersonCreate(firstname="Jane", lastname="Doe")
    person_db1 = create_person_db(session=session, person=person1)
    person_db2 = create_person_db(session=session, person=person2)

    persons_from_db = read_persons_db(session=session)
    assert len(persons_from_db) == 2

    delete_person_db(session=session, person_id=person_db1.id)
    persons_from_db = read_persons_db(session=session)
    assert len(persons_from_db) == 1
    assert persons_from_db[0].firstname == "Jane"

def test_udpate_person_db_updates_person(session: Session):
    person = PersonCreate(firstname="John", lastname="Doe")
    person_db = create_person_db(session=session, person=person)
    person_update = PersonUpdate(firstname="Jane", lastname="Doe")
    person_db = update_person_db(session=session, person_id=person_db.id, person=person_update)
    assert person_db.firstname == "Jane"
    assert person_db.lastname == "Doe"
    assert person_db.date_of_birth == None
    assert person_db.is_in_contact == False

def test_udpate_person_db_returns_none_when_invalid_id(session: Session):
    person_update = PersonUpdate(firstname="Jane", lastname="Doe")
    person_db = update_person_db(session=session, person_id=1, person=person_update)
    assert person_db == None