from src.schemas.comments_schem import CommentResponse, CommentCreate
from fastapi import HTTPException, APIRouter, status, Depends
from src.api.depends import comment_use_cases
from typing import List
from src.domain.comment.comment_use_cases import CommentUseCases
from src.core.exceptions.domain_exceptions import CommentMemeException, CommentNotFoundByIdException, PostNotFoundByIdException
from src.services.auth_serv import AuthService
from src.schemas.users_schem import UserResponse

router = APIRouter()


@router.post("/comments", status_code=status.HTTP_201_CREATED, response_model=CommentResponse, tags=["Comments"])
async def create_comment(
    data: CommentCreate,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: CommentUseCases = Depends(comment_use_cases)
):
    try:
        return await service.create(data)
    except CommentMemeException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse], tags=["Comments"])
async def get_post_comments(
    post_id: int,
    service: CommentUseCases = Depends(comment_use_cases)
):
    try:
        return await service.get_by_post(post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
async def delete_comment(
    comment_id: int,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: CommentUseCases = Depends(comment_use_cases)
):
    try:
        await service.delete(comment_id)
        return None
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
