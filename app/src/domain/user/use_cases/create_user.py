from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.infrastructure.sqlite.models.users import UserModel
from src.schemas.users import UserCreate
from datetime import datetime


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, data: UserCreate) -> UserCreate:
        with self._database.session() as session:
            existing = self._repo.get_by_username(session, data.username)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists"
                )

            user = UserModel(
                username=data.username,
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                password=data.password,
                is_staff=data.is_staff,
                is_active=data.is_active,
                is_superuser=data.is_superuser,
                last_login=datetime.now(),
                date_joined=datetime.now()
            )

            created = self._repo.create(session, user)
            return UserCreate.model_validate(created, from_attributes=True)
