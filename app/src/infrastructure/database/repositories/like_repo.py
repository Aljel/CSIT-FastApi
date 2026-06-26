from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.models.like_model import PostLikeModel


class LikeRepository:
    def get_by_post_user(
        self, session: Session, post_id: int, user_id: int
    ) -> Optional[PostLikeModel]:
        return (
            session.query(PostLikeModel)
            .filter(PostLikeModel.post_id == post_id, PostLikeModel.user_id == user_id)
            .first()
        )

    def get_user_liked_ids(self, session: Session, user_id: int) -> list[int]:
        rows = (
            session.query(PostLikeModel.post_id)
            .filter(PostLikeModel.user_id == user_id)
            .all()
        )
        return [r[0] for r in rows]

    def get_likes_count(self, session: Session, post_id: int) -> int:
        return (
            session.query(PostLikeModel)
            .filter(PostLikeModel.post_id == post_id)
            .count()
        )
