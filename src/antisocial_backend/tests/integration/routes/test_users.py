import pytest 
from pytest import fixture
from fastapi.testclient import TestClient
from antisocial_backend.dependencies.dependencies import get_session
from sqlmodel import Session,SQLModel,create_engine, StaticPool
from sqlmodel.pool import StaticPool
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate

def test_users_get_returns_200(client: TestClient):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [{"username": "Rick"}, {"username": "Morty"}]

def test_users_post_returns_200(client: TestClient):
    response = client.post("/users/",
                           json={
                               "email_address": "asdf@asdf.com",
                                "password": "asdf"
                                })
    assert response.status_code == 200
    assert response.json() == {"result": "user created"}

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

def test_users_get_by_id_returns_200(client: TestClient):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"username": "Rick"}


def test_users_put_by_id_returns_200(client: TestClient):
    response = client.put("/users/1")
    assert response.status_code == 200
    assert response.json() == {"result": "user updated"}

def test_users_delete_by_id_returns_200(client: TestClient):    
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"result": "user deleted"}