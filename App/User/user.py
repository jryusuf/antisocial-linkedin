from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from datetime import datetime

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)
    password: str
    creadted_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)
    is_active: bool = Field(default=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True)

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(UserBase):
    id: int
