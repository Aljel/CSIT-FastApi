from typing import Type, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.users_model import UserModel


class UserRepository:
    def __init__(self):
        self._model: Type[UserModel] = UserModel

    def get_by_id(self, session: Session, user_id: int) -> Optional[UserModel]:
        return session.query(self._model).filter(self._model.id == user_id).first()

    def get_by_username(self, session: Session, username: str) -> Optional[UserModel]:
        return session.query(self._model).filter(self._model.username == username).first()

    def create(self, session: Session, user: UserModel) -> UserModel:
        session.add(user)
        session.flush()
        return user

    def update(self, session: Session, user: UserModel, update_data: dict) -> UserModel:
        for key, value in update_data.items():
            setattr(user, key, value)
        session.flush()
        return user

    def delete(self, session: Session, user: UserModel) -> None:
        session.delete(user)
        session.flush()
