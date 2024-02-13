from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlalchemy.sql import func
class UserBase(SQLModel):
    pass
class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True,default=None)
    email_address: EmailStr = Field(sa_type=AutoString)
    password: str = ...
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    is_active: Optional[bool] = Field(default=False)

class UserCreate(UserBase):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    password: str = Field(..., min_length=3)

    @field_validator("password")
    def check_passsword(cls, value):
        value = str(value)
        if len(value)<8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")
        return value


class UserRead(UserBase):
    email_address: EmailStr = Field(primary_key=True,sa_type=AutoString)
    created_at: datetime
    updated_at: datetime
    is_active: bool

class UserUpdate(UserBase):
    email_address: Optional[EmailStr] = Field(sa_type=AutoString)
    password: Optional[str] = Field(min_length=3)
    is_active: Optional[bool]

    @field_validator("password")
    def check_passsword(cls, value):
        value = str(value)
        if len(value)<8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number")
        return value