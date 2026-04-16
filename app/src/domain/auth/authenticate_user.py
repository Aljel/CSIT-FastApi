import logging

from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.users_repo import UserRepository
from src.schemas.users_schem import UserBase as UserSchema
from src.resources.auth import verify_password
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.core.exceptions.domain_exceptions import UserNotFoundByUsernameException, WrongPasswordException

logger = logging.getLogger(__name__)


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self,
        login: str,
        password: str,
    ) -> UserSchema:
        try:
            with self._database.session() as session:
                user = self._repo.get(session=session, login=login)
        except UserNotFoundException:
            error = UserNotFoundByLoginException(login=login)
            logger.error(error.get_detail())
            raise error

        if not verify_password(plain_password=password, hashed_password=user.password):
            error = WrongPasswordException()
            logger.error(error.get_detail())
            raise error

        return UserSchema.model_validate(obj=user)
