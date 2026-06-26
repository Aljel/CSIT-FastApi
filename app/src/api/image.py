from fastapi import HTTPException, APIRouter, status, Depends, UploadFile, File
from typing import List
from src.schemas.image_schem import PostImageResponse, CommentImageResponse
from src.api.depends import image_use_cases
from src.domain.image.image_use_cases import ImageUseCases
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    CommentNotFoundByIdException,
)
from src.services.auth_serv import AuthService
from src.schemas.users_schem import UserResponse

router = APIRouter(tags=["Images"])


@router.post(
    "/posts/{post_id}/images",
    response_model=List[PostImageResponse],
    status_code=status.HTTP_201_CREATED,
)
async def upload_post_images(
    post_id: int,
    files: List[UploadFile] = File(...),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: ImageUseCases = Depends(image_use_cases),
):
    try:
        return service.upload_post_images(post_id, files, current_user.id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/posts/{post_id}/images", response_model=List[PostImageResponse])
async def get_post_images(
    post_id: int,
    service: ImageUseCases = Depends(image_use_cases),
):
    return service.get_post_images(post_id)


@router.delete(
    "/posts/{post_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post_image(
    post_id: int,
    image_id: int,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: ImageUseCases = Depends(image_use_cases),
):
    try:
        service.delete_post_image(image_id, current_user.id)
        return None
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.post(
    "/comments/{comment_id}/images",
    response_model=List[CommentImageResponse],
    status_code=status.HTTP_201_CREATED,
)
async def upload_comment_images(
    comment_id: int,
    files: List[UploadFile] = File(...),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: ImageUseCases = Depends(image_use_cases),
):
    try:
        return service.upload_comment_images(comment_id, files, current_user.id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/comments/{comment_id}/images", response_model=List[CommentImageResponse])
async def get_comment_images(
    comment_id: int,
    service: ImageUseCases = Depends(image_use_cases),
):
    return service.get_comment_images(comment_id)


@router.delete(
    "/comments/{comment_id}/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment_image(
    comment_id: int,
    image_id: int,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: ImageUseCases = Depends(image_use_cases),
):
    try:
        service.delete_comment_image(image_id, current_user.id)
        return None
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
