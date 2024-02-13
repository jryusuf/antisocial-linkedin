from antisocial_backend.models.User import User,UserCreate,UserRead,UserUpdate
from antisocial_backend.dependencies.dependencies import Session, get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
## def method(input:type)->output:type:
##     pass



#convert the password to a stronger hash
def create_user_db(*,session: Session = Depends(get_session),user: UserCreate)-> UserRead:
    db_user = User.model_validate(user)
    db_user_exist = session.exec(select(User).where(User.email_address == db_user.email_address)).first()
    if db_user_exist:
        raise ValueError("Email already exists")
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def read_users_db(*,session: Session = Depends(get_session))-> list[UserRead]:
    return session.exec(select(User)).all()