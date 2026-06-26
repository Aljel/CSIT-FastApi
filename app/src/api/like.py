from fastapi import HTTPException, APIRouter, status, Depends
from src.schemas.like_schem import LikeToggleRequest, LikeToggleResponse
from src.api.depends import like_use_cases
from src.domain.like.like_use_cases import LikeUseCases
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.services.auth_serv import AuthService
from src.schemas.users_schem import UserResponse

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/toggle", response_model=LikeToggleResponse)
async def toggle_like(
    data: LikeToggleRequest,
    current_user: UserResponse = Depends(AuthService.get_current_user),
    service: LikeUseCases = Depends(like_use_cases),
):
    try:
        return await service.toggle(post_id=data.post_id, user_id=current_user.id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.get_detail()
        )
