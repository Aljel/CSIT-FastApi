from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status


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

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isupper() for char in value):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву.")
        return value

    @field_validator("username", mode="after")
    @staticmethod
    def check_login(username: str) -> str:
        if any(x in username for x in "!@#$%^&*№;%:?"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Имя пользователя не должно содержать специальных символов"
            )

        return username


class UserResponse(UserBase):
    id: int
    is_staff: bool
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime]
    date_joined: datetime
    model_config = ConfigDict(from_attributes=True)
