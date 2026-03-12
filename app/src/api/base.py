from fastapi import APIRouter, status, HTTPException, Depends

from src.schemas.posts import PostCreate, PostResponse
from src.schemas.users import UserResponse, UserCreate, UserBase
from src.domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase
from src.api.depends import get_user_by_username_use_case, create_user_use_case

router = APIRouter()


@router.get("/user/{username}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_login(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(
        get_user_by_username_use_case)
) -> UserResponse:
    user = await use_case.execute(username=username)

    return user


@router.post("/user", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def create_user(
    data: UserCreate,
    use_case: CreateUserUseCase = Depends(create_user_use_case)
) -> UserBase:
    return await use_case.execute(data)


@router.post("/test_json", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def test_json(post: PostCreate) -> dict:
    if len(post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    response = {
        "post_text": post.text,
        "author_name": post.author.username
    }

    return PostResponse.model_validate(obj=response)
