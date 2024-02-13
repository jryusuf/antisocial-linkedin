from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr

class UserCreate(SQLModel, table=True):
    email_address: str = Field(primary_key=True)
    password: str = ...