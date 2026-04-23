from typing import Annotated

from fastapi import Depends
from pydantic import SecretStr
from jose import JWTError, jwt

from src.core.exceptions.auth_exceptions import CredentialsException
from src.core.exceptions.database_exceptions import UserNotFoundException
from src.schemas.users_schem import UserBase as UserSchema
from src.resources.auth_res import oauth2_scheme
from src.infrastructure.sqlite.database import database as sqlite_database, Database
from src.infrastructure.sqlite.repositories.users_repo import UserRepository

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
SECRET_AUTH_KEY = SecretStr(
    "aF75A92Cd9s10KGL4nLdt1r85XRtZ7APNO6NheGeKdRBhhc9oObQywxmqPF")
AUTH_ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        _database: Database = sqlite_database
        _repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        except JWTError:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        try:
            with _database.session() as session:
                user = _repo.get_by_username(
                    session=session, username=username)
        except UserNotFoundException:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)

        return UserSchema.model_validate(obj=user, from_attributes=True)
