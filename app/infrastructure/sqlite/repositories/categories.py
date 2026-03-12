from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.models import Category


class CategoryRepository:
    def __init__(self):
        self._model: Type[Category] = Category

    def list_all(self, session: Session) -> List[Category]:
        return session.query(self._model).where(self._model.is_published == True).all()

    def get_by_slug(self, session: Session, slug: str) -> Optional[Category]:
        return session.query(self._model).where(self._model.slug == slug).scalar()
