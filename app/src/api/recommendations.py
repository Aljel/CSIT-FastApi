from fastapi import APIRouter, Depends, Query
from src.domain.recommendation.recommendation_use_cases import RecommendationUseCases
from src.schemas.posts_schem import PostResponse
from src.api.depends import recommendation_use_cases
from src.services.auth_serv import AuthService
from src.schemas.users_schem import UserResponse

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/trending", response_model=list[PostResponse])
def trending(
    limit: int = Query(10, ge=1, le=50),
    use_cases: RecommendationUseCases = Depends(recommendation_use_cases),
):
    return use_cases.get_trending(limit=limit)


@router.get("/similar/{post_id}", response_model=list[PostResponse])
def similar(
    post_id: int,
    limit: int = Query(5, ge=1, le=50),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_cases: RecommendationUseCases = Depends(recommendation_use_cases),
):
    return use_cases.get_similar(post_id, limit=limit, user_id=current_user.id)


@router.get("", response_model=list[PostResponse])
def personalized(
    limit: int = Query(10, ge=1, le=50),
    current_user: UserResponse = Depends(AuthService.get_current_user),
    use_cases: RecommendationUseCases = Depends(recommendation_use_cases),
):
    return use_cases.get_personalized(current_user.id, limit=limit)
