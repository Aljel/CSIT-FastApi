from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.categories_model import CategoryModel


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int) -> Optional[CategoryModel]:
        return session.query(self._model).filter(self._model.id == category_id).first()

    def get_all(self, session: Session) -> List[CategoryModel]:
        return session.query(self._model).all()

    def create(self, session: Session, category: CategoryModel) -> CategoryModel:
        session.add(category)
        session.flush()
        return category

    def delete(self, session: Session, category: CategoryModel) -> None:
        session.delete(category)
        session.flush()
