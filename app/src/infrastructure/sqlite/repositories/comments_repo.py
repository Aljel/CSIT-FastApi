from typing import Type, List
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models import Comment


class CommentRepository:
    def __init__(self):
        self._model: Type[Comment] = Comment

    def get_by_post_id(self, session: Session, post_id: int) -> List[Comment]:
        query = (
            session.query(self._model)
            .where(self._model.post_id == post_id)
            .order_by(self._model.created_at.asc())
        )
        return query.all()

    def create(self, session: Session, comment_obj: Comment) -> Comment:
        session.add(comment_obj)
        session.commit()
        return comment_obj
