from fastapi import HTTPException, status
from datetime import datetime
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repo import UserRepository
from src.infrastructure.sqlite.models.users_model import UserModel
from src.schemas.users_schem import UserCreate, UserResponse


class UserUseCases:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def create(self, data: UserCreate) -> UserResponse:
        with self._database.session() as session:
            existing = self._repo.get_by_username(session, data.username)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists"
                )

            user = UserModel(
                **data.model_dump(exclude={"password"}),
                password=data.password,
                last_login=datetime.now(),
                date_joined=datetime.now()
            )

            created = self._repo.create(session, user)
            return UserResponse.model_validate(created, from_attributes=True)

    async def get_by_username(self, username: str) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.get_by_username(session, username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return UserResponse.model_validate(user, from_attributes=True)

    async def delete(self, user_id: int) -> None:
        with self._database.session() as session:
            user = self._repo.get_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            self._repo.delete(session, user)
