from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import EmailStr


##This is the User model and it is used to create a user object
##We will have different like base, create, read, update, delete
##may be some helper models as well

class UserBase(SQLModel):
    email_adress: EmailStr = ...
    password: str = ...
    is_active: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now()
    

    