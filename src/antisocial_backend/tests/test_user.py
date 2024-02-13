import pytest
from pytest import fixture
from antisocial_backend.models.User import UserBase,User
from datetime import datetime

@pytest.fixture(name="userbase")
def user_base():
    return UserBase(
        email_adress="asd@asd.com",
        password="1234")

@pytest.fixture(name="user")
def user():
    return User(
        id = 1,
        email_adress="asd@asd.com",
        password="1234")


def test_When_UserBaseIsCreated_Then_ItIsCreated(userbase: user_base):
    assert userbase is not None

def test_When_UserBaseIsCreated_Then_IsActiveIsFalse(userbase: user_base):
    assert userbase.is_active == False

def test_When_UserBaseUpdateIsActive_Then_IsActiveIsTrue(userbase: user_base):
    userbase.is_active = True
    assert userbase.is_active == True

def test_When_UserBaseIsCreated_Then_CreatedAtIsNow(userbase: user_base):
    assert userbase.created_at is not None

def test_When_GivenUserBase_CreatedAt_Is_Timestamp(userbase: user_base):
    assert userbase.created_at is not None
    assert type(userbase.created_at) == datetime

def test_When_GivenUserBase_Then_UpdatedAtIsNotNone(userbase: user_base):
    assert userbase.updated_at is not None

def test_When_GivenUser_Then_User_IsInstanceOfUserBase(user: user):
    assert isinstance(user, UserBase)

def test_When_GivenUser_Then_User_HasId(user: user):
    assert type(user.id) == int