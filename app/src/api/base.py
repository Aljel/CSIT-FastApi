from fastapi import APIRouter, status, HTTPException, Depends

from src.schemas.posts import PostCreate, PostResponse
from src.schemas.users import UserResponse
from src.domain.user.use_cases.get_user_by_login import GetUserByLoginUseCase
from api.depends import get_get_user_by_login_use_case

router = APIRouter()


@router.get("/user/{login}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_login(
    login: str,
    use_case: GetUserByLoginUseCase = Depends(get_get_user_by_login_use_case)
) -> UserResponse:
    user = await use_case.execute(login=login)

    return user


@router.post("/test_json", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def test_json(post: PostCreate) -> dict:
    if len(post.text) < 3:
        raise HTTPException(
            detail="Длина поста должна быть не меньше 3 символов",
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    response = {
        "post_text": post.text,
        "author_name": post.author.login
    }

    return PostResponse.model_validate(obj=response)
