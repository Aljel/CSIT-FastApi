from pydantic import BaseModel, EmailStr, Field, SecretStr
from datetime import date, datetime
from typing import Optional


class User(BaseModel):
    username: str
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[EmailStr]
    passwd: SecretStr
    is_staff: bool
    is_active: bool
    is_superuser: bool
    last_login: datetime
    date_joined: date
