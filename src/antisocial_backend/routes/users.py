from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.models.User import UserCreate, User,UserRead, UserUpdate
from antisocial_backend.dependencies.dependencies import get_session, Session
from antisocial_backend.dependencies.database.users import *


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[UserRead])
async def read_users(*,session:Session = Depends(get_session)):
    users = read_users_db(session=session)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@router.get("/{user_id}" , response_model=UserRead)
async def read_user(*,session:Session = Depends(get_session)
                    ,user_id: int):
    user = read_user_db(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    
@router.post("/", response_model=UserRead)
async def create_user(*, session:Session= Depends(get_session)
                      ,user: UserCreate):
    try:
        return create_user_db(session=session,user=user)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.put("/{user_id}", response_model=UserRead)
async def update_user(*,session:Session=Depends(get_session)
                      ,user_id: int, user: UserUpdate):
    db_user = update_user_db(session=session,user_id=user_id,user=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}")
async def delete_user(*,session:Session=Depends(get_session)
                      ,user_id: int):
    if not delete_user_db(session=session,user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"result": "user deleted"}

