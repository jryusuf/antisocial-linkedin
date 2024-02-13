import pytest
from pytest import fixture
from antisocial_backend.models.User import UserBase
from datetime import datetime

@pytest.fixture(name="user")
def user():
    return UserBase(
        email_adress="asd@asd.com",
        password="1234")


def test_When_UserBaseIsCreated_Then_ItIsCreated(user: user):
    assert user is not None

def test_When_UserBaseIsCreated_Then_IsActiveIsFalse(user: user):
    assert user.is_active == False

def test_When_UserBaseUpdateIsActive_Then_IsActiveIsTrue(user: user):
    user.is_active = True
    assert user.is_active == True

def test_When_UserBaseIsCreated_Then_CreatedAtIsNow(user: user):
    assert user.created_at is not None

def test_When_GivenUserBase_CreatedAt_Is_Timestamp(user: user):
    assert user.created_at is not None
    assert type(user.created_at) == datetime

