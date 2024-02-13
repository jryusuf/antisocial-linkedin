from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr


##This is the User model and it is used to create a user object
##We will have different like base, create, read, update, delete
##may be some helper models as well

class UserBase(SQLModel):
    email_adress: EmailStr = Field(unique=True, index =True, sa_type=AutoString)
    password: str = ...
    is_active: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

class User(UserBase, table=True):
    id: int = Field(min_length=1,primary_key=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    pass