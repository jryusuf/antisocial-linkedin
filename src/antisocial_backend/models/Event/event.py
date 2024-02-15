from typing import Optional
from sqlmodel import Field, SQLModel, AutoString
from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlalchemy.sql import func

class EventBase(SQLModel):
    type: str = Field(..., min_length=3)
    name: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3)
    start_date: datetime = None

class Event(EventBase, table=True):
    id: Optional[int] = Field(primary_key=True,default=None)

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int

class EventUpdate(EventBase):
    pass

class EventDelete(EventBase):
    pass
