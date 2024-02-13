import pytest
from pytest import fixture
from antisocial_backend.models.User import UserBase

@pytest.fixture(name="user")
def user():
    return UserBase(
        email_adress="asd@asd.com",
        password="1234")


def test_When_UserBaseIsCreated_Then_ItIsCreated(user: user):
    assert user is not None

def test_When_UserBaseIsCreated_Then_IsActiveIsFalse(user: user):
    assert user.is_active == False