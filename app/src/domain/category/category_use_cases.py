import logging
from fastapi import HTTPException, status
from typing import List
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.categories_repo import CategoryRepository
from src.infrastructure.database.models.categories_model import CategoryModel
from src.schemas.categoties_schem import CategoryCreate, CategoryUpdate, CategoryResponse
from src.core.exceptions.database_exceptions import CategoryNotFoundException, CategoryAlreadyExistsException, CategoryRandomException
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException, CategoryMemeException, CategoryNameIsNotUniqueException

logger = logging.getLogger(__name__)


class CategoryUseCases:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def create(self, data: CategoryCreate) -> CategoryResponse:
        category = CategoryModel(**data.model_dump())
        try:
            with self._database.session() as session:
                created = self._repo.create(session, category)
                logger.info(
                    f"Категория '{created.title}' создана (ID: {created.id})")
                return CategoryResponse.model_validate(created, from_attributes=True)
        except CategoryAlreadyExistsException:
            logger.error(f"Категория '{category.title}' уже существует")
            raise CategoryNameIsNotUniqueException(title=category.title)

    async def get_all(self) -> List[CategoryResponse]:
        try:
            with self._database.session() as session:
                categories = self._repo.get_all(session)
                return [CategoryResponse.model_validate(c, from_attributes=True) for c in categories]
        except CategoryRandomException:
            raise CategoryMemeException()

    async def update(self, category_id: int, data: CategoryUpdate) -> CategoryResponse:
        update_data = data.model_dump(exclude_unset=True)
        try:
            with self._database.session() as session:
                category = self._repo.get_by_id(session, category_id)
                if category is None:
                    raise CategoryNotFoundByIdException(id=category_id)
                updated = self._repo.update(
                    session, category, update_data)
                logger.info(f"Категория ID {category_id} обновлена")
                return CategoryResponse.model_validate(updated, from_attributes=True)
        except CategoryNotFoundException:
            raise CategoryNotFoundByIdException(id=category_id)
        except CategoryAlreadyExistsException:
            raise CategoryNameIsNotUniqueException(
                title=data.title or "")

    async def delete(self, category_id: int) -> None:
        try:
            with self._database.session() as session:
                category = session.query(CategoryModel).filter(
                    CategoryModel.id == category_id).first()
                if category is None:
                    raise CategoryNotFoundByIdException(id=category_id)
                session.delete(category)
                logger.info(f"Категория ID {category_id} удалена")
        except CategoryNotFoundException:
            logger.error(f"Ошибка при удалении категории: {
                         CategoryNotFoundException}")
            raise CategoryNotFoundByIdException(id=category_id)
