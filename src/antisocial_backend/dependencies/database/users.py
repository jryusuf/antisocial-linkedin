from antisocial_backend.models.User import *
from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
## def method(input:type)->output:type:
##     pass



#convert the password to a stronger hash
def create_user_db(*,session: Session = Depends(get_session)
                   ,user: UserCreate)-> UserRead:
    db_user = User.model_validate(user)
    db_user_exist = session.exec(select(User)
                                 .where(User
                                        .email_address == db_user.email_address)
                                        ).first()
    if db_user_exist:
        raise ValueError("Email already exists")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def read_users_db(*,session: Session = Depends(get_session))-> list[UserRead]:
    return session.exec(select(User)).all()

def read_user_db(*,session: Session = Depends(get_session)
                 ,user_id: int)-> UserRead:
    user = session.get(User, user_id)
    return user

def delete_user_db(*,session: Session = Depends(get_session)
                   ,user_id: int)-> bool:
    if isinstance(user_id, int) is False:
        raise ValueError("Invalid user_id")
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

def update_user_db(*,session: Session = Depends(get_session)
                   ,user_id: int, user: UserUpdate)-> UserRead:
    if isinstance(user_id, int) is False:
        raise ValueError("Invalid user_id")
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user