from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlalchemy.sql import func

class PersonBase(SQLModel):
    firstname: str = ...
    lastname: str = ...
    date_of_birth: Optional[datetime] = None
    is_in_contact: bool = False

class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class PersonCreate(PersonBase):
    pass

class PersonRead(PersonBase):
    id: int

class PersonUpdate(PersonBase):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    is_in_contact: Optional[bool] = None

class PersonDelete(PersonBase):
    pass

