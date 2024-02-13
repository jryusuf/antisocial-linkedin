import pytest
from sqlmodel import Session
from pydantic import ValidationError
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead
from antisocial_backend.dependencies.database.users import create_user_db

def test_create_user_db_creates_user(session: Session):
    user = UserCreate(email_address="asd@asd.com",password="asdf")
    user = create_user_db(session=session,user=user)
    new_user = session.get(User,user.id)
    assert new_user is not None
    assert new_user.email_address == user.email_address
    assert new_user.password == user.password

def test_create_user_db_raises_error_when_email_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdf")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd@asd.com",password="asdf")
    with pytest.raises(ValueError):
        db_user2 = create_user_db(session=session,user=user2)


def test_create_user_db_returns_new_user_when_email_not_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdf")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd2@asd.com",password="asdf")
    db_user2 = create_user_db(session=session,user=user2)

    assert db_user2 is not None

def test_create_user_db_raises_error_when_email_invalid(session: Session):
    with pytest.raises(ValueError):
        user1 = UserCreate(email_address="asd",password="asdf")
        db_user1 = create_user_db(session=session,user=user1)

def test_create_user_db_raises_error_when_password_invalid(session: Session):
    with pytest.raises(ValueError):
        user1 = UserCreate(email_address="asdf@adf.com",password="ad")

def test_create_user_db_raises_error_when_password_and_email_invalid(session: Session):
    with pytest.raises(ValueError):
        user1 = UserCreate(email_address="asd",password="ad")