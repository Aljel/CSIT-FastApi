from typing import Type, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.users_model import UserModel


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_username(self, session: Session, username: str) -> Optional[UserModel]:
        query = (
            session.query(self._model)
            .where(self._model.username == username)
        )
        return query.scalar()

    def get_by_id(self, session: Session, user_id: int) -> Optional[UserModel]:
        return session.query(self._model).where(self._model.id == user_id).scalar()

    def create(self, session: Session, user: UserModel) -> UserModel:
        session.add(user)
        session.flush()
        session.commit()
        return user
