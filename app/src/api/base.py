from fastapi import APIRouter, status, Depends, HTTPException
from src.schemas.categoties_schem import CategoryResponse, CategoryCreate
from src.api.depends import category_use_cases
from src.domain.category.category_use_cases import CategoryUseCases
from typing import List
from src.api.user import router as user_router
from src.api.post import router as post_router
from src.api.comment import router as comment_router
from src.core.exceptions.domain_exceptions import CategoryNotFoundByIdException, CategoryMemeException, CategoryNameIsNotUniqueException


router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)
router.include_router(comment_router)


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse, tags=["Categories"])
async def create_category(
    data: CategoryCreate,
    service: CategoryUseCases = Depends(category_use_cases)
):
    try:
        return await service.create(data)
    except CategoryNameIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.get("/categories", response_model=List[CategoryResponse], tags=["Categories"])
async def list_categories(
    service: CategoryUseCases = Depends(category_use_cases)
):
    try:
        return await service.get_all()
    except CategoryMemeException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categories"])
async def delete_category(
    category_id: int,
    service: CategoryUseCases = Depends(category_use_cases)
):
    try:
        await service.delete(category_id)
        return None
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
