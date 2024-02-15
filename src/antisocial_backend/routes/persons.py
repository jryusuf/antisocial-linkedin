from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.models.User import UserCreate, User,UserRead, UserUpdate
from antisocial_backend.dependencies.dependencies import get_session, Session
from antisocial_backend.dependencies.database.persons import *

router = APIRouter(
    prefix="/persons",
    tags=["persons"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[PersonRead])
async def read_persons(*,session:Session = Depends(get_session)):
    persons = read_persons_db(session=session)
    if not persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons

@router.get("/{person_id}" , response_model=PersonRead)
async def read_person(*,session:Session = Depends(get_session), person_id: int):
    person = read_person_db(session=session, person_id=person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/", response_model=PersonRead)
async def create_person(*, session:Session= Depends(get_session), person: PersonCreate):
    return create_person_db(session=session,person=person)

@router.put("/{person_id}", response_model=PersonRead)
async def update_person(*,session:Session=Depends(get_session),person_id: int, person: PersonUpdate):
    db_person = update_person_db(session=session,person_id=person_id, person=person)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/{person_id}")
async def delete_person(*,session:Session=Depends(get_session),person_id: int):
    if not delete_person_db(session=session,person_id=person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return {"result": "person deleted"}
