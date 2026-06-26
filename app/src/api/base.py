from fastapi import APIRouter
from src.api.user import router as user_router
from src.api.post import router as post_router
from src.api.comment import router as comment_router
from src.api.auth import router as auth_router
from src.api.category import router as category_router
from src.api.recommendations import router as recommendations_router
from src.api.like import router as like_router
from src.api.image import router as image_router

router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)
router.include_router(comment_router)
router.include_router(auth_router)
router.include_router(category_router)
router.include_router(recommendations_router)
router.include_router(like_router)
router.include_router(image_router)
