from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.dependencies.dependencies import get_token_header
from antisocial_backend.models.User import UserCreate, User,UserRead, UserUpdate
from antisocial_backend.dependencies.dependencies import get_session, Session
from sqlmodel import select
from antisocial_backend.dependencies.database.users import create_user_db
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[UserRead])
async def read_users(*,session:Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@router.get("/{user_id}" , response_model=UserRead)
async def read_user(*,session:Session = Depends(get_session),user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@router.post("/", response_model=UserRead)
async def create_user(*, session:Session= Depends(get_session),user: UserCreate):
    try:
        return create_user_db(session=session,user=user)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/{user_id}", response_model=UserRead)
async def update_user(*,session:Session=Depends(get_session),user_id: int, user: UserUpdate):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(*,session:Session=Depends(get_session),user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"result": "user deleted"}

