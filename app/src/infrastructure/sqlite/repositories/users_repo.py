from typing import Type
from sqlalchemy.orm import session
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from src.infrastructure.sqlite.models.users_model import UserModel
from src.core.exceptions.database_exceptions import UserNotFoundException, UserAlreadyExistsException


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_username(self, session: session, username: str) -> UserModel:
        query = (
            select(self._model)
            .where(self._model.username == username)
        )

        try:
            user = session.scalar(query)
            session.flush()
            return user
        except IntegrityError:
            raise UserNotFoundException()

    def create(self, session: session, user: UserModel) -> UserModel:
        try:
            session.add(user)
            session.flush()
            return user
        except IntegrityError:
            raise UserAlreadyExistsException()

    def delete(self, session: session, user: UserModel) -> None:
        try:
            session.delete(user)
            session.flush()
        except IntegrityError:
            raise UserNotFoundException()
