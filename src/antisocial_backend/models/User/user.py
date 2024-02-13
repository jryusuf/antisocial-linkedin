from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr

class UserBase(SQLModel):
    pass
class User(UserBase, table=True):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    password: str = ...

class UserCreate(UserBase):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    password: str = ...