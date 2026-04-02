from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.categories_repo import CategoryRepository
from src.infrastructure.sqlite.models.categories_model import CategoryModel
from src.schemas.categoties_schem import CategoryCreate, CategoryResponse


class CategoryUseCases:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def create(self, data: CategoryCreate) -> CategoryResponse:
        with self._database.session() as session:
            category = CategoryModel(**data.model_dump())
            created = self._repo.create(session, category)
            return CategoryResponse.model_validate(created, from_attributes=True)

    async def get_all(self) -> List[CategoryResponse]:
        with self._database.session() as session:
            categories = self._repo.get_all(session)
            return [CategoryResponse.model_validate(c, from_attributes=True) for c in categories]

    async def delete(self, category_id: int) -> None:
        with self._database.session() as session:
            category = session.query(CategoryModel).filter(
                CategoryModel.id == category_id).first()
            if not category:
                raise HTTPException(
                    status_code=404, detail="Category not found")
            session.delete(category)
