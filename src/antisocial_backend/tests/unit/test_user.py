import pytest
from pytest import fixture
from antisocial_backend.models.User import UserCreate, UserRead
from datetime import datetime
from pydantic import ValidationError

def test_user_create():
    user = UserCreate(email_address="asdf@asdf.com",password="asdfA1234")
    assert user is not None

def test_user_create_invalid_email_raise_error():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asdf",password="asdf")

def test_user_create_empty_password_raise_error():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asdf@adf.com")

#todo add more validation tests

def test_user_read_has_email_adress():
    user = UserRead(
        email_address="adf@asdf.com",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True)
    
    assert user.email_address == "adf@asdf.com"