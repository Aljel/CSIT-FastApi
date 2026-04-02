from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    is_staff: bool = False
    is_active: bool = True
    is_superuser: bool = False
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    id: int
    is_staff: bool
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    date_joined: datetime
    model_config = ConfigDict(from_attributes=True)
