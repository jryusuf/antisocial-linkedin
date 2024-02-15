import pytest
from pytest import fixture
from antisocial_backend.models.User import UserCreate, UserRead,UserUpdate
from datetime import datetime
from pydantic import ValidationError
from antisocial_backend.models.Organization import *

def test_org_create_model_has_type_name_and_start_date():
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    assert org.type is not None
    assert org.name is not None
    assert org.start_date is not None

def test_org_create_model_raises_validation_error_when_type_is_empty():
    with pytest.raises(ValidationError):
        org = OrganizationCreate(type="",name="The Red Cross",start_date=datetime.now())

def test_org_create_model_raises_validation_error_when_name_is_empty():
    with pytest.raises(ValidationError):
        org = OrganizationCreate(type="non-profit",name="",start_date=datetime.now())

def test_org_create_model_raises_validation_error_when_start_date_is_empty():
    with pytest.raises(ValidationError):
        org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=None)

def test_org_create_model_return_address_when_address_is_provided():
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now(),address="123 Main St")
    assert org.address == "123 Main St"

def test_org_read_model_has_type_name_start_date_and_id():
    org = OrganizationRead(type="non-profit",name="The Red Cross",start_date=datetime.now(),id=1)
    assert org.type is not None
    assert org.name is not None
    assert org.start_date is not None
    assert org.id is not None

def test_org_delete_model_has_type_name_start_date():
    org = OrganizationDelete(type="non-profit",name="The Red Cross",start_date=datetime.now(),id=1)
    assert org.type is not None
    assert org.name is not None
    assert org.start_date is not None

def test_org_update_model_has_type_name_start_date():
    org = OrganizationUpdate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    assert org.type is not None
    assert org.name is not None
    assert org.start_date is not None

def test_org_model_has_type_name_start_date_and_id():
    org = Organization(type="non-profit",name="The Red Cross",start_date=datetime.now(),id=1)
    assert org.type is not None
    assert org.name is not None
    assert org.start_date is not None
    assert org.id is not None