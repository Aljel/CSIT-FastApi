from fastapi import APIRouter, status, Depends
from src.schemas.comments_schem import CommentResponse, CommentCreate
from src.api.depends import comment_use_cases
from src.domain.comment.comment_use_cases import CommentUseCases
from src.schemas.categoties_schem import CategoryResponse, CategoryCreate
from src.api.depends import category_use_cases
from src.domain.category.category_use_cases import CategoryUseCases
from typing import List
from src.api.user import router as user_router
from src.api.post import router as post_router


router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)


@router.post("/comments", status_code=status.HTTP_201_CREATED, response_model=CommentResponse, tags=["Comments"])
async def create_comment(
    data: CommentCreate,
    service: CommentUseCases = Depends(comment_use_cases)
):
    return await service.create(data)


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse], tags=["Comments"])
async def get_post_comments(
    post_id: int,
    service: CommentUseCases = Depends(comment_use_cases)
):
    return await service.get_by_post(post_id)


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
async def delete_comment(
    comment_id: int,
    service: CommentUseCases = Depends(comment_use_cases)
):
    await service.delete(comment_id)
    return None


@router.post("/categories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse, tags=["Categories"])
async def create_category(
    data: CategoryCreate,
    service: CategoryUseCases = Depends(category_use_cases)
):
    return await service.create(data)


@router.get("/categories", response_model=List[CategoryResponse], tags=["Categories"])
async def list_categories(
    service: CategoryUseCases = Depends(category_use_cases)
):
    return await service.get_all()


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categories"])
async def delete_category(
    category_id: int,
    service: CategoryUseCases = Depends(category_use_cases)
):
    await service.delete(category_id)
    return None
