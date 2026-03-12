from typing import Type, Optional
from sqlalchemy.orm import Session
from src.models import User


class UserRepository:
    def __init__(self):
        self._model: Type[User] = User

    def get_by_username(self, session: Session, username: str) -> Optional[User]:
        query = (
            session.query(self._model)
            .where(self._model.username == username)
        )
        return query.scalar()

    def get_by_id(self, session: Session, user_id: int) -> Optional[User]:
        return session.query(self._model).where(self._model.id == user_id).scalar()
