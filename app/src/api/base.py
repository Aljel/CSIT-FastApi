from fastapi import APIRouter
from src.api.user import router as user_router
from src.api.post import router as post_router
from src.api.comment import router as comment_router
from src.api.auth import router as auth_router
from src.api.category import router as category_router


router = APIRouter()
router.include_router(user_router)
router.include_router(post_router)
router.include_router(comment_router)
router.include_router(auth_router)
router.include_router(category_router)
