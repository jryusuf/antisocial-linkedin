import pytest
from sqlmodel import Session, select
from antisocial_backend.tests.integration.fixtures import session_fixture,client_fixture
from antisocial_backend.models.Person import PersonCreate, Person, PersonRead, PersonUpdate
from antisocial_backend.dependencies.database.organizations import *
from datetime import datetime

def test_create_org_db_creates_org(session: Session):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    org_from_db = session.get_one(Organization, org_db.id)
    assert org_from_db.type == "non-profit"
    assert org_from_db.name == "The Red Cross"
    assert org_from_db.start_date != None

def test_read_orgs_db_returns_list_of_orgs(session: Session):
    org1 = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org2 = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db1 = create_organization_db(session=session, org=org1)
    org_db2 = create_organization_db(session=session, org=org2)

    orgs = read_organizations_db(session=session)
    assert len(orgs) == 2
    assert orgs[0].type == "non-profit"
    assert orgs[1].type == "univercity"

def test_read_orgs_db_returns_empty_list(session: Session):
    orgs = read_organizations_db(session=session)
    assert len(orgs) == 0

def test_read_org_db_returns_org(session: Session):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    org_from_db = read_organization_db(session=session, org_id=org_db.id)
    assert org_from_db.type == "non-profit"
    assert org_from_db.name == "The Red Cross"
    assert org_from_db.start_date != None

def test_read_org_db_returns_none_with_invalid_id(session: Session):
    org_from_db = read_organization_db(session=session, org_id=1)
    assert org_from_db == None

def test_delete_org_db_deletes_org(session: Session):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)
    orgs_from_db = read_organizations_db(session=session)
    assert len(orgs_from_db) == 1

    delete_req = delete_organization_db(session=session, org_id=org_db.id)
    orgs_from_db = read_organizations_db(session=session)
    assert len(orgs_from_db) == 0
    assert delete_req == True

def test_delete_org_db_returns_false_when_org_not_found(session: Session):
    result = delete_organization_db(session=session, org_id=1)
    assert result == False

def test_delete_org_db_deletes_correct_org(session: Session):
    org1 = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org2 = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db1 = create_organization_db(session=session, org=org1)
    org_db2 = create_organization_db(session=session, org=org2)

    orgs_from_db = read_organizations_db(session=session)
    assert len(orgs_from_db) == 2

    delete_req = delete_organization_db(session=session, org_id=org_db1.id)
    orgs_from_db = read_organizations_db(session=session)
    assert len(orgs_from_db) == 1
    assert delete_req == True
    assert orgs_from_db[0].type == "univercity"

def test_update_org_db_updates_org(session: Session):
    org = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org_db = create_organization_db(session=session, org=org)

    org_update = OrganizationUpdate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db = update_organization_db(session=session, org_id=org_db.id, org=org_update)

    org_from_db = read_organization_db(session=session, org_id=org_db.id)
    assert org_from_db.type == "univercity"
    assert org_from_db.name == "The Red Cross"
    assert org_from_db.start_date != None

def test_update_org_db_returns_none_with_invalid_id(session: Session):
    org_update = OrganizationUpdate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db = update_organization_db(session=session, org_id=1, org=org_update)
    assert org_db == None

def test_update_org_db_updates_correct_org(session: Session):
    org1 = OrganizationCreate(type="non-profit",name="The Red Cross",start_date=datetime.now())
    org2 = OrganizationCreate(type="univercity",name="The Red Cross",start_date=datetime.now())
    org_db1 = create_organization_db(session=session, org=org1)
    org_db2 = create_organization_db(session=session, org=org2)

    org_update = OrganizationUpdate(type="corporation",name="The Red Cross",start_date=datetime.now())
    org_db = update_organization_db(session=session, org_id=org_db2.id, org=org_update)

    org_from_db = read_organization_db(session=session, org_id=org_db2.id)
    assert org_from_db.type == "corporation"
    assert org_from_db.name == "The Red Cross"
    assert org_from_db.start_date != None
    assert org_from_db.id == org_db2.id