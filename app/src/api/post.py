from fastapi import HTTPException, APIRouter, status, Depends
from typing import List
from src.schemas.posts_schem import PostResponse, PostCreate
from src.api.depends import post_use_cases
from src.domain.post.post_use_cases import PostUseCases
from src.core.exceptions.domain_exceptions import PostNameIsNotUniqueException, PostNotFoundByIdException, PostMemeException
from src.services.auth_serv import AuthService


router = APIRouter()


@router.get("/posts", response_model=List[PostResponse], tags=["Posts"])
async def list_posts(
    limit: int = 10,
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        return await service.get_all(limit)
    except PostMemeException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.get("/posts/{post_id}", response_model=PostResponse, tags=["Posts"])
async def get_post(
    post_id: int,
    current_user: PostResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        return await service.get_by_id(post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse, tags=["Posts"])
async def create_post(
    data: PostCreate,
    current_user: PostResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        return await service.create(data)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
async def delete_post(
    post_id: int,
    current_user: PostResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        await service.delete(post_id)
        return None
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
