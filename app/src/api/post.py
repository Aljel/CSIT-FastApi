from fastapi import HTTPException, APIRouter, status, Depends
from typing import List
from src.schemas.posts_schem import PostResponse, PostCreate, PostUpdate
from src.api.depends import post_use_cases
from src.domain.post.post_use_cases import PostUseCases
from src.core.exceptions.domain_exceptions import PostNameIsNotUniqueException, PostNotFoundByIdException, PostMemeException
from src.services.auth_serv import AuthService
from src.schemas.users_schem import UserResponse


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
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        return await service.get_by_id(post_id, user_id=current_user.id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse, tags=["Posts"])
async def create_post(
    data: PostCreate,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        return await service.create(data)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.put("/posts/{post_id}", response_model=PostResponse, tags=["Posts"])
async def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        has_non_like_fields = any(
            getattr(data, field_name) is not None
            for field_name in data.model_fields
            if field_name != "is_liked"
        )
        if has_non_like_fields:
            post = await service.get_by_id(post_id)
            if post.author_id != current_user.id:
                raise HTTPException(
                    status_code=403, detail="Недостаточно прав для редактирования этого поста")
        return await service.update(post_id, data, user_id=current_user.id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
    except PostNameIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
async def delete_post(
    post_id: int,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: PostUseCases = Depends(post_use_cases)
):
    try:
        await service.delete(post_id)
        return None
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
