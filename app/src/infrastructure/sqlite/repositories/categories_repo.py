from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.categories_model import CategoryModel
from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException, CategoryRandomException
from sqlalchemy.exc import IntegrityError


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int) -> Optional[CategoryModel]:
        try:
            return session.query(self._model).filter(self._model.id == category_id).first()
        except IntegrityError:
            raise CategoryNotFoundException()

    def get_all(self, session: Session) -> List[CategoryModel]:
        try:
            return session.query(self._model).all()
        except IntegrityError:
            raise CategoryRandomException()

    def create(self, session: Session, category: CategoryModel) -> CategoryModel:
        try:
            session.add(category)
            session.flush()
            return category
        except IntegrityError:
            raise CategoryAlreadyExistsException

    def delete(self, session: Session, category: CategoryModel) -> None:
        try:
            session.delete(category)
            session.flush()
        except IntegrityError:
            raise CategoryNotFoundException()
