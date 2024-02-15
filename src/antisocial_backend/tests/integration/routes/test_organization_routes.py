from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.User import UserCreate, User, UserRead
from antisocial_backend.models.Person import PersonCreate, Person, PersonRead, PersonUpdate
from antisocial_backend.dependencies.database.organizations import *
from datetime import datetime

def test_read_orgs_return_404_when_there_is_no_org(session: Session, client: TestClient):
    response = client.get("/organizations")
    assert response.status_code == 404
    assert response.json() == {"detail": "Organizations not found"}

def test_read_orgs_return_orgs(session: Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    response = client.get("/organizations")
    assert response.status_code == 200

    data = response.json()

    assert data[0]["type"] == "non-profit"
    assert data[0]["name"] == "The Red Cross"
    assert data[0]["start_date"] != None
    assert data[0]["id"] == 1

def test_read_orgs_return_multiple_orgs_when_exits(session:Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    org = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    response = client.get("/organizations")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["type"] == "non-profit"
    assert data[1]["type"] == "univercity"


def test_read_org_return_404_when_org_not_found(session: Session, client: TestClient):
    response = client.get("/organizations/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Organization not found"}

def test_read_org_return_org(session: Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    response = client.get("/organizations/1")
    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "non-profit"
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 1

def test_read_org_return_correct_org_when_multiple_exists(session: Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    org = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    response = client.get("/organizations/2")
    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "univercity"
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 2

def test_delete_org_return_404_when_org_not_found(session: Session, client: TestClient):
    response = client.delete("/organizations/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Organization not found"}

def test_delete_org_deletes_org_if_exits(session:Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    response = client.delete("/organizations/1")
    assert response.status_code == 200
    assert response.json() == {"result": "organization deleted"}

    read_from_db = read_organization_db(session=session, org_id=1)
    assert read_from_db == None

def test_delete_org_deletes_correct_org_if_multiple_orgs_exists(session:Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    org = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    response = client.delete("/organizations/2")
    assert response.status_code == 200
    assert response.json() == {"result": "organization deleted"}

    read_from_db = read_organization_db(session=session, org_id=2)
    assert read_from_db == None
    read_from_db_2 = read_organization_db(session=session, org_id=1)
    assert read_from_db_2 != None

def test_create_org_returns_org(session: Session, client: TestClient):
    response = client.post("/organizations/", json={
        "type": "non-profit",
        "name": "The Red Cross",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "non-profit"
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 1

def test_create_org_raises_error_when_given_invalid_input(session: Session, client: TestClient):
    response = client.post("/organizations/", json={
        "type": "non-profit",
        "start_date": str(datetime.now())
    })
    assert response.status_code == 422

def test_update_org_returns_422_when_given_invalid_input(session: Session, client: TestClient):
    response = client.put("/organizations/1", json={})
    assert response.status_code == 422

def test_update_org_updates_org_when_it_exits(session: Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    response = client.put("/organizations/1", json={
        "type": "univercity",
        "name": "The Red Cross",
        "start_date": str(datetime.now()),
    })
    assert response.status_code == 200
    data = response.json()

    assert data["type"] == "univercity"
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None

def test_update_org_updates_correct_org_when_multiple_exits(session: Session, client: TestClient):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    create_organization_db(session=session, org=org)

    org = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    response = client.put("/organizations/2", json={
        "type": "corporation",
        "name": "The Red Cross",
        "start_date": str(datetime.now()),
    })
    assert response.status_code == 200
    data = response.json()

    assert data["type"] == "corporation"
    assert data["name"] == "The Red Cross"
    assert data["start_date"] != None
    assert data["id"] == 2
    assert data["id"] != 1