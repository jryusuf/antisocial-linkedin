import pytest
from pytest import fixture
from antisocial_backend.models.User import UserCreate, UserRead,UserUpdate
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

def test_user_create_raises_error_when_password_is_less_than_8_characters():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asdf@asdf.com,password=asdfA1")

def test_user_create_raises_error_when_password_does_not_contain_uppercase_letter():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="adf@asdf.com",password="asdf1234")

def test_user_create_raises_error_when_password_does_not_contain_lowercase_letter():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asd@af.com",password="ASDF1234")

def test_user_create_raises_error_when_password_does_not_contain_number():
    with pytest.raises(ValidationError):
        user = UserCreate(email_address="asd@asd.com",password="ASDFasdf")

def test_user_update_raises_error_when_password_is_less_than_8_characters():
    with pytest.raises(ValidationError):
        user = UserUpdate(email_address="asd@asd.com",password="asdfA1")

def test_user_update_raises_error_when_password_does_not_contain_uppercase_letter():
    with pytest.raises(ValidationError):
        user = UserUpdate(email_address="asdf@asdf.com",password="asdf1234")
    
def test_user_update_raises_error_when_password_does_not_contain_lowercase_letter():
    with pytest.raises(ValidationError):
        user = UserUpdate(email_address="asd@asd.com",password="ASDF1234")

def test_user_update_raises_error_when_password_does_not_contain_number():
    with pytest.raises(ValidationError):
        user = UserUpdate(email_address="ad@adf.com",password="ASDFasdf")
