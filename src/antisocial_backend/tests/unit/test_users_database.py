import pytest
from sqlmodel import Session
from pydantic import ValidationError
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead
from antisocial_backend.dependencies.database.users import create_user_db,read_users_db,read_user_db

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

def test_read_users_db_returns_zero_user_when_empty(session: Session):
    users = read_users_db(session=session)
    assert len(users) == 0

def test_read_users_db_returns_one_user_when_one_exists(session: Session):
    user = User(email_address="asd@asd.com",password="asdf")
    session.add(user)
    session.commit()
    users = read_users_db(session=session)
    assert len(users) == 1

def test_read_users_db_returns_list_of_User(session: Session):
    user = User(email_address="asd@asd.com",password="asdf")
    session.add(user)
    session.commit()
    users = read_users_db(session=session)
    assert isinstance(users[0],User)

def test_read_users_db_returns_two_users_when_two_exists(session: Session):
    user1 = User(email_address="asd@asd.com",password="asdf")
    user2 = User(email_address="asdf@asdf.com",password="asdf")
    session.add(user1)
    session.add(user2)
    session.commit()
    users = read_users_db(session=session)
    assert len(users) == 2

def test_read_user_by_id_returns_user(session: Session):
    user = User(email_address="asd@asd.com",password="asdf")
    session.add(user)
    session.commit()
    user_db = read_user_db(session=session,user_id=user.id)
    assert user_db is not None
    assert user_db.email_address == user.email_address

def test_read_user_by_id_returns_none_when_user_not_found(session: Session):
    user = User(email_address="asd@asds.com",password="asdf")
    session.add(user)
    session.commit()
    user_db = read_user_db(session=session,user_id=2)
    assert user_db is None