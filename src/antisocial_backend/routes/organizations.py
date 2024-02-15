from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.models.User import UserCreate, User,UserRead, UserUpdate
from antisocial_backend.dependencies.dependencies import get_session, Session
from antisocial_backend.dependencies.database.organizations import *

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[OrganizationRead])
async def read_organizations(*,session:Session = Depends(get_session)):
    orgs = read_organizations_db(session=session)
    if not orgs:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return orgs

@router.get("/{org_id}" , response_model=OrganizationRead)
async def read_organization(*,session:Session= Depends(get_session) ,org_id: int):
    org = read_organization_db(session=session, org_id=org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.post("/", response_model=OrganizationRead)
async def create_organization(*, session: Session = Depends(get_session),org: OrganizationCreate):
    return create_organization_db(session=session,org=org)

@router.put("/{org_id}", response_model=OrganizationRead)
async def update_organization(*, session: Session = Depends(get_session),org_id:int, org: OrganizationUpdate):
    db_org = update_organization_db(session=session,org_id=org_id,org=org)
    if not db_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_org

@router.delete("/{org_id}")
async def delete_organization(*, session: Session = Depends(get_session),org_id: int):
    if not delete_organization_db(session=session,org_id=org_id):
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"result": "organization deleted"}
