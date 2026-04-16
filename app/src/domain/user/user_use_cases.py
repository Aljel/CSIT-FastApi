from src.infrastructure.sqlite.database import database
from datetime import datetime
from src.infrastructure.sqlite.repositories.users_repo import UserRepository
from src.schemas.users_schem import UserCreate, UserResponse
from src.infrastructure.sqlite.models.users_model import UserModel
from src.core.exceptions.database_exceptions import UserAlreadyExistsException, UserNotFoundException
from src.core.exceptions.domain_exceptions import UserUsernameIsNotUniqueException, UserNotFoundByUsernameException
from src.resources.auth import get_password_hash


class UserUseCases:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def create(self, data: UserCreate) -> UserResponse:
        user_model = UserModel(
            **data.model_dump(exclude={"password"}),
            password=get_password_hash(password=data.password),
            last_login=datetime.now(),
            date_joined=datetime.now()
        )
        try:
            with self._database.session() as session:
                user = self._repo.create(session, user_model)
                return UserResponse.model_validate(user, from_attributes=True)
        except UserAlreadyExistsException:
            raise UserUsernameIsNotUniqueException(
                username=user_model.username)

    async def get_by_username(self, username: str) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                return UserResponse.model_validate(user, from_attributes=True)
        except UserNotFoundException:
            raise UserNotFoundByUsernameException(username=username)

    async def delete(self, username: str) -> None:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                self._repo.delete(session, user)
        except UserNotFoundException:
            raise UserNotFoundByUsernameException(username=username)
