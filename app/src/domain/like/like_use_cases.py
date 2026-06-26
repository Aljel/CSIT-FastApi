from datetime import datetime
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.like_repo import LikeRepository
from src.infrastructure.database.repositories.posts_repo import PostRepository
from src.infrastructure.database.models.like_model import PostLikeModel
from src.schemas.like_schem import LikeToggleResponse
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException
from src.infrastructure.database.models.posts_model import PostModel


class LikeUseCases:
    def __init__(self):
        self._database = database
        self._like_repo = LikeRepository()
        self._post_repo = PostRepository()

    async def toggle(self, post_id: int, user_id: int) -> LikeToggleResponse:
        with self._database.session() as session:
            post = self._post_repo.get_by_id(session, post_id)
            if post is None:
                raise PostNotFoundByIdException(id=post_id)

            like = self._like_repo.get_by_post_user(session, post_id, user_id)
            if like:
                session.delete(like)
                is_liked = False
            else:
                session.add(
                    PostLikeModel(
                        post_id=post_id,
                        user_id=user_id,
                        created_at=datetime.now(),
                    )
                )
                is_liked = True

            likes_count = self._like_repo.get_likes_count(session, post_id)
            return LikeToggleResponse(is_liked=is_liked, likes_count=likes_count)
