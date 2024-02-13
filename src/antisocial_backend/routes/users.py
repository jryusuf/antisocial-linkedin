from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.dependencies.dependencies import get_token_header
from antisocial_backend.models.User import UserCreate, User,UserRead
from antisocial_backend.dependencies.dependencies import get_session, Session
from sqlmodel import select

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[UserRead])
async def read_users(
    *,
    session:Session = Depends(get_session)
):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users

@router.get("/{user_id}" , response_model=UserRead)
async def read_user(
    *,
    session:Session = Depends(get_session),
    user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@router.post("/")
async def create_user(
    *, 
    session:Session = Depends(get_session),
    user: UserCreate):

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"result": "user created"}

@router.put("/{user_id}")
async def update_user(user_id: int):
    return {"result": "user updated"}

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"result": "user deleted"}

