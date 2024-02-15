from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlalchemy.sql import func

class OrganizationBase(SQLModel):
    type: str = Field(...,min_length=3)
    name: str = Field(...,min_length=3)
    start_date: datetime = ...
    address: Optional[str] = None

class Organization(OrganizationBase, table=True):
    id: Optional[int] = Field(primary_key=True,default=None)

class OrganizationCreate(OrganizationBase):
    pass
    
class OrganizationRead(OrganizationBase):
    id: int = ...

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationDelete(OrganizationBase):
    pass

