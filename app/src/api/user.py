from fastapi import APIRouter, status, Depends, HTTPException
from src.schemas.users_schem import UserResponse, UserCreate
from src.api.depends import user_use_cases
from src.domain.user.user_use_cases import UserUseCases
from src.core.exceptions.domain_exceptions import UserUsernameIsNotUniqueException, UserNotFoundByUsernameException

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse, tags=["Users"])
async def create_user(
    data: UserCreate,
    service: UserUseCases = Depends(user_use_cases)
):
    try:
        return await service.create(data)
    except UserUsernameIsNotUniqueException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=exc.get_detail())


@router.get("/users/{username}", response_model=UserResponse, tags=["Users"])
async def get_user(
    username: str,
    service: UserUseCases = Depends(user_use_cases)
):
    try:
        return await service.get_by_username(username)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
async def delete_user(
    username: str,
    service: UserUseCases = Depends(user_use_cases)
):
    try:
        await service.delete(username)
        return None
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail())
