from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.sql import func
class UserBase(SQLModel):
    pass
class User(UserBase, table=True):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    password: str = ...
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_active: Optional[bool] = Field(default=False)

class UserCreate(UserBase):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    password: str = Field(..., min_length=3)

class UserRead(UserBase):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    created_at: datetime
    updated_at: datetime
    is_active: bool