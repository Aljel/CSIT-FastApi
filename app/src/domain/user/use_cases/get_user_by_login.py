from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User as UserBase


class GetUserByLoginUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, login: str) -> UserBase:
        with self._database.session() as session:
            user = self._repo.get(session=session, login=login)

        return UserBase.model_validate(obj=user)
