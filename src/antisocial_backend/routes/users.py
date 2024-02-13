from fastapi import APIRouter,HTTPException,Depends
from antisocial_backend.dependencies.dependencies import get_token_header
from antisocial_backend.models.User import UserCreate
from antisocial_backend.dependencies.dependencies import get_session, Session

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/{user_id}")
async def read_user(user_id: int):
    return {"username": "Rick"}

@router.post("/")
async def create_user(
    *, 
    session:Session = Depends(get_session),
    user: UserCreate):
    
    db_user = UserCreate.model_validate(user)
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

