import pytest
from sqlmodel import Session
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

def test_create_user_db_returns_none_when_email_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdf")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd@asd.com",password="asdf")
    db_user2 = create_user_db(session=session,user=user2)

    assert db_user2 is None

def test_create_user_db_returns_new_user_when_email_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdf")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd2@asd.com",password="asdf")
    db_user2 = create_user_db(session=session,user=user2)

    assert db_user2 is not None