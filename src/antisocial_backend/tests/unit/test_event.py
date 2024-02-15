import pytest
from pytest import fixture
from datetime import datetime
from pydantic import ValidationError
from antisocial_backend.models.Event import *

def test_event_create_model_returns_type_name_description_date():
    event = EventCreate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    assert event.type == "non-profit"
    assert event.name == "The Red Cross"
    assert event.description == "A non-profit organization"
    assert event.start_date != None

def test_event_create_model_raises_error_when_type_is_less_than_3_chars():
    with pytest.raises(ValidationError) as e:
        event = EventCreate(
            type="no",
            name="The Red Cross",
            description="A non-profit organization",
            start_date=datetime.now())
        
def test_event_create_model_raises_error_when_name_is_less_than_3_chars():
    with pytest.raises(ValidationError) as e:
        event = EventCreate(
            type="non-profit",
            name="Th",
            description="A non-profit organization",
            start_date=datetime.now())
        
def test_event_create_model_raises_error_when_description_is_less_than_3_chars():
    with pytest.raises(ValidationError) as e:
        event = EventCreate(
            type="non-profit",
            name="The Red Cross",
            description="An",
            start_date=datetime.now())
        
def test_event_read_model_returns_type_name_description_date_id():
    event = EventRead(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now(),
        id=1)
    
    assert event.type == "non-profit"
    assert event.name == "The Red Cross"
    assert event.description == "A non-profit organization"
    assert event.start_date != None
    assert event.id == 1

def test_event_update_model_returns_type_name_description_date():
    event = EventUpdate(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    assert event.type == "non-profit"
    assert event.name == "The Red Cross"
    assert event.description == "A non-profit organization"
    assert event.start_date != None

def test_event_delete_model_returns_type_name_description_date():
    event = EventDelete(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now())
    
    assert event.type == "non-profit"
    assert event.name == "The Red Cross"
    assert event.description == "A non-profit organization"
    assert event.start_date != None

def test_event_model_returns_type_name_description_date_id():
    event = Event(
        type="non-profit",
        name="The Red Cross",
        description="A non-profit organization",
        start_date=datetime.now(),
        id=1)
    
    assert event.type == "non-profit"
    assert event.name == "The Red Cross"
    assert event.description == "A non-profit organization"
    assert event.start_date != None
    assert event.id == 1