import logging
from src.infrastructure.database.database import database
from datetime import datetime
from src.infrastructure.database.repositories.users_repo import UserRepository
from src.schemas.users_schem import UserCreate, UserUpdate, UserResponse
from src.infrastructure.database.models.users_model import UserModel
from src.core.exceptions.database_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    UserUsernameIsNotUniqueException,
    UserNotFoundByUsernameException,
)
from src.resources.auth_res import get_password_hash

logger = logging.getLogger(__name__)


class UserUseCases:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def create(self, data: UserCreate) -> UserResponse:
        print(data.password)
        user_model = UserModel(
            **data.model_dump(exclude={"password"}),
            password=get_password_hash(password=data.password),
            last_login=datetime.now(),
            date_joined=datetime.now(),
        )
        print(user_model.password)
        try:
            with self._database.session() as session:
                user = self._repo.create(session, user_model)
                logger.info(f"Создан пользователь: {
                            user.username} (ID: {user.id})")
                return UserResponse.model_validate(user, from_attributes=True)
        except UserAlreadyExistsException:
            logger.error(f"Ошибка регистрации: имя {data.username} уже занято")
            raise UserUsernameIsNotUniqueException(username=user_model.username)

    async def get_by_username(self, username: str) -> UserResponse:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                return UserResponse.model_validate(user, from_attributes=True)
        except UserNotFoundException:
            logger.error(f"Пользователь {username} не найден")
            raise UserNotFoundByUsernameException(username=username)

    async def update(self, username: str, data: UserUpdate) -> UserResponse:
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"] is not None:
            update_data["password"] = get_password_hash(
                password=update_data["password"]
            )
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                updated = self._repo.update(session, user, update_data)
                logger.info(f"Пользователь {username} обновлен")
                return UserResponse.model_validate(updated, from_attributes=True)
        except UserNotFoundException:
            raise UserNotFoundByUsernameException(username=username)
        except UserAlreadyExistsException:
            raise UserUsernameIsNotUniqueException(username=username)

    async def delete(self, username: str) -> None:
        try:
            with self._database.session() as session:
                user = self._repo.get_by_username(session, username)
                self._repo.delete(session, user)
                logger.info(f"Пользователь {username} был удален")
        except UserNotFoundException:
            logger.error(f"Попытка удаления: пользователь {
                         username} не найден")
            raise UserNotFoundByUsernameException(username=username)
