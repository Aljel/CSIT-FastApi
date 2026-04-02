from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repo import UserRepository
from src.schemas.users_schem import UserResponse
from fastapi import HTTPException, status


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponse:
        with self._database.session() as session:
            user = self._repo.get_by_username(
                session=session, username=username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found"
            )

        return UserResponse.model_validate(obj=user)
