import pytest
from pytest import fixture
from antisocial_backend.models.User import UserCreate
from datetime import datetime
from pydantic import ValidationError

def test_user_create():
    user = UserCreate(email_address="asdf@asdf.com",password="asdf")
    assert user is not None

def test_user_create_invalid_email_raise_error():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asdf",password="asdf")

def test_user_create_empty_password_raise_error():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asdf@adf.com")