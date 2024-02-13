from fastapi.testclient import TestClient
from sqlmodel import Session
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead

def test_users_get_returns_404_when_there_is_no_user(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 404

def test_users_get_users_returns_200(session: Session,client: TestClient):
    user = User(email_address="asdf@adsf.com",password="asdf")
    session.add(user)
    session.commit()
    response = client.get("/users/")
    assert response.status_code == 200

def test_users_post_returns_200(client: TestClient):
    response = client.post("/users/",
                           json={
                               "email_address": "asdf@asdf.com",
                                "password": "asdf"
                                })
    assert response.status_code == 200

def test_users_get_by_id_returns_404_when_user_not_found(client: TestClient):
    response = client.get("/users/1")
    assert response.status_code == 404

def test_users_get_by_id_returns_200_when_user_found(session: Session,client: TestClient):
    user = User(email_address="asd@asd.com",password="asdf")
    session.add(user)
    session.commit()
    response = client.get("/users/1")

    data = response.json()

    assert response.status_code == 200
    assert data["email_address"] == user.email_address
    assert data["is_active"] == user.is_active


def test_users_post_returns_422_when_invalid_email(client: TestClient):
    response = client.post("/users/",
                           json={
                               "email_address": "asdf",
                                "password": "asdf"
                                })
    assert response.status_code == 422

def test_users_post_returns_422_when_password_lenght_less_than_3(client: TestClient):
    response = client.post("/users/",
                           json={
                               "email_address": "adsq@fad.com",
                               "password": "ad"})
    assert response.status_code == 422

def test_users_post_returns_422_when_empty_password(client: TestClient):
    response = client.post("/users/",
                           json={
                               "email_address": "adq@fasdf.com"})
    assert response.status_code == 422

def test_users_put_by_id_returns_404_when_user_is_not_found(client: TestClient):
    response = client.put("/users/1",
                          json={"email_address": "asd@asd.com",
                                "password": "asdf",
                                "is_active": True})
    assert response.status_code == 404

def test_users_put_by_id_returns_200_when_user_is_found(session: Session,client: TestClient):
    user = User(email_address="asdf@asdf.com",password="asdf")
    session.add(user)
    session.commit()
    response = client.put("/users/1",
                           json={
                               "email_address": "asdf2@asdf.com",
                                "password": "asdf2",
                                "is_active": True})

    assert response.status_code == 200
    assert session.get(User, user.id).email_address == "asdf2@asdf.com"
    assert session.get(User, user.id).password == "asdf2"
    assert session.get(User, user.id).is_active == True
     

def test_users_delete_by_id_returns_404_when_user_is_not_found(client: TestClient):    
    response = client.delete("/users/1")
    assert response.status_code == 404

def test_users_delete_the_user_if_exits(session: Session,client: TestClient):
    user = User(email_address="asd@asd.com",password="asdf")
    session.add(user)
    session.commit()
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"result": "user deleted"}
    assert session.get(User, user.id) is None