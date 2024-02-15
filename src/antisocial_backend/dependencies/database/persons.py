from antisocial_backend.models.Person import *
from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select


def create_person_db(*,
                     session: Session = Depends(get_session),
                     person: PersonCreate)-> PersonRead:
    db_person = Person.model_validate(person)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person

def read_persons_db(*,
                    session: Session = Depends(get_session))-> list[PersonRead]:
    return session.exec(select(Person)).all()

def read_person_db(*,
                   session: Session = Depends(get_session),
                  person_id: int)-> PersonRead:
    person = session.get(Person, person_id)
    return person

def delete_person_db(*,
                     session: Session = Depends(get_session),
                     person_id: int)-> bool:
    person_db = session.get(Person, person_id)
    if not person_db:
        return False
    session.delete(person_db)
    return True

def update_person_db(*,session: Session = Depends(get_session),person_id:int, person:PersonUpdate)-> PersonRead:
    db_person = session.get(Person, person_id)
    if not db_person:
        return None
    person_data = person.model_dump(exclude_unset=True)
    for key, value in person_data.items():
        setattr(db_person, key, value)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person
