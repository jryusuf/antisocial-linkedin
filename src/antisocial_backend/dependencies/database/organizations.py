from antisocial_backend.models.Organization import *
from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

def create_organization_db(*, session: Session, org: OrganizationCreate):
    db_org = Organization.model_validate(org)
    session.add(db_org)
    session.commit()
    session.refresh(db_org)
    return db_org

def read_organizations_db(*, session: Session)-> list[OrganizationRead]:
    return session.exec(select(Organization)).all()

def read_organization_db(*, session: Session, org_id: int)-> OrganizationRead:
    org = session.get(Organization, org_id)
    return org

def delete_organization_db(*, session: Session, org_id: int)-> bool:
    org_db = session.get(Organization, org_id)
    if not org_db:
        return False
    session.delete(org_db)
    return True

def update_organization_db(*, session: Session, org_id:int, org:OrganizationUpdate)-> OrganizationRead:
    db_org = session.get(Organization, org_id)
    if not db_org:
        return None
    org_data = org.model_dump(exclude_unset=True)
    for key, value in org_data.items():
        setattr(db_org, key, value)
    session.add(db_org)
    session.commit()
    session.refresh(db_org)
    return db_org
