import pytest
from pytest import fixture
from datetime import datetime
from pydantic import ValidationError
from antisocial_backend.models.Person import PersonCreate, Person, PersonUpdate, PersonDelete

def test_person_create_raises_error_when_first_name_is_empty():
    with pytest.raises(ValidationError):
        person = PersonCreate()

def test_person_create_raises_error_when_last_name_is_empty():
    with pytest.raises(ValidationError):
        person = PersonCreate(firstname="John")

def test_person_create_a_person_when_only_given_first_and_last_name():
    person = PersonCreate(firstname="John", lastname="Doe")
    assert person is not None
    assert person.firstname == "John"
    assert person.lastname == "Doe"

def test_person_create_a_person_when_given_first_and_last_name_dob_is_none():
    person = PersonCreate(firstname="John", lastname="Doe", date_of_birth=None)
    assert person is not None
    assert person.date_of_birth == None

def test_person_create_a_person_when_given_first_and_last_name_dob_is_not_none():
    person = PersonCreate(firstname="John", lastname="Doe", date_of_birth=datetime.now())
    assert person is not None
    assert person.date_of_birth is not None
    assert isinstance(person.date_of_birth, datetime)

def test_person_create_returns_in_contact_boolean():
    person = PersonCreate(firstname="John", lastname="Doe", date_of_birth=datetime.now())
    assert person.is_in_contact == False

def test_person_create_returns_true_when_is_in_contact_is_true():
    person = PersonCreate(firstname="John", lastname="Doe", date_of_birth=datetime.now(), is_in_contact=True)
    assert person.is_in_contact == True

def test_person_update_takes_input_all_optional():
    person = PersonUpdate()
    assert person is not None

def test_person_update_returns_correct_values_with_given_input():
    person = PersonUpdate(firstname="John", lastname="Doe", date_of_birth=datetime.now(), is_in_contact=True)
    assert person.firstname == "John"
    assert person.lastname == "Doe"
    assert person.date_of_birth is not None
    assert person.is_in_contact == True

def test_person_have_id():
    person = Person(id=1,firstname="John", lastname="Doe")
    assert person.id is not None

