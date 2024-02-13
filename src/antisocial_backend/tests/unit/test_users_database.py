import pytest
from sqlmodel import Session, select
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead, UserUpdate
from antisocial_backend.dependencies.database.users import *


def test_create_user_db_creates_user(session: Session):
    user = UserCreate(email_address="asd@asd.com",password="asdfA1234")
    user = create_user_db(session=session,user=user)
    new_user = session.get(User,user.id)
    assert new_user is not None
    assert new_user.email_address == user.email_address
    assert new_user.password == user.password

def test_create_user_db_raises_error_when_email_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdfA1234")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd@asd.com",password="asdfA1234")
    with pytest.raises(ValueError):
        db_user2 = create_user_db(session=session,user=user2)


def test_create_user_db_returns_new_user_when_email_not_exists(session: Session):
    user1 = UserCreate(email_address="asd@asd.com",password="asdfA1234")
    db_user1 = create_user_db(session=session,user=user1)

    user2 = UserCreate(email_address="asd2@asd.com",password="asdfA1234")
    db_user2 = create_user_db(session=session,user=user2)

    assert db_user2 is not None

def test_create_user_db_raises_error_when_email_invalid(session: Session):
    with pytest.raises(ValueError):
        db_user1 = create_user_db(session=session,user=UserCreate(email_address="asd",password="asdfA1234"))

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
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    users = read_users_db(session=session)
    assert len(users) == 1

def test_read_users_db_returns_list_of_User(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    users = read_users_db(session=session)
    assert isinstance(users[0],User)

def test_read_users_db_returns_two_users_when_two_exists(session: Session):
    user1 = User(email_address="asd@asd.com",password="asdfA1234")
    user2 = User(email_address="asdf@asdf.com",password="asdfA1234")
    session.add(user1)
    session.add(user2)
    session.commit()
    users = read_users_db(session=session)
    assert len(users) == 2

def test_read_user_by_id_returns_user(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = read_user_db(session=session,user_id=user.id)
    assert user_db is not None
    assert user_db.email_address == user.email_address

def test_read_user_by_id_returns_none_when_user_not_found(session: Session):
    user = User(email_address="asd@asds.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = read_user_db(session=session,user_id=2)
    assert user_db is None

def test_delete_user_by_id_deletes_user(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = session.get(User,user.id)
    assert user_db is not None
    delete_user_db(session=session,user_id=user.id)
    users = session.exec(select(User)).all()
    assert len(users) == 0
    

def test_delete_user_by_id_returns_true_when_user_deleted(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = session.get(User,user.id)
    assert user_db is not None
    result = delete_user_db(session=session,user_id=user.id)
    assert result == True

def test_delete_user_by_id_returns_false_when_user_not_found(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = session.get(User,user.id)
    assert user_db is not None
    result = delete_user_db(session=session,user_id=2)
    assert result == False

def test_delete_user_by_id_raises_error_when_user_id_invalid(session: Session):
    with pytest.raises(ValueError):
        delete_user_db(session=session,user_id="a")

def test_update_user_by_id_updates_user(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = session.get(User,user.id)
    assert user_db is not None
    new_user_info = UserUpdate(email_address="asd2@asd.com",password="asdfA1234", is_active=True)
    update_user_db(session=session,user_id=user.id,user=new_user_info)
    user_db = session.get(User,user.id)
    assert user_db.email_address == new_user_info.email_address

def test_update_user_by_id_returns_none_when_user_not_found(session: Session):
    user = User(email_address="asd@asd.com",password="asdfA1234")
    session.add(user)
    session.commit()
    user_db = session.get(User,user.id)
    assert user_db is not None
    new_user_info = UserUpdate(email_address="asd2@asd.com",password="asdfA1234", is_active=True)
    user_db = update_user_db(session=session,user_id=2,user=new_user_info)
    assert user_db is None

def test_update_user_by_id_raises_error_when_user_id_invalid(session: Session):
    with pytest.raises(ValueError):
        new_user_info = UserUpdate(email_address="asd@asd.com",password="asdfA1234", is_active=True)
        user_db = update_user_db(session=session,user_id="a",user=new_user_info)