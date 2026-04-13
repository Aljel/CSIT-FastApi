from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.comments_model import CommentModel
from src.core.exceptions.database_exceptions import CommentNotFoundException, CommentRandomException
from sqlalchemy.exc import IntegrityError


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel

    def get_by_id(self, session: Session, comment_id: int) -> Optional[CommentModel]:
        try:
            return session.query(self._model).filter(self._model.id == comment_id).first()
        except IntegrityError:
            raise CommentNotFoundException()

    def get_by_post_id(self, session: Session, post_id: int) -> List[CommentModel]:
        try:
            return (session.query(self._model)
                    .filter(self._model.post_id == post_id)
                    .order_by(self._model.created_at.asc()).all())
        except IntegrityError:
            raise CommentNotFoundException()

    def create(self, session: Session, comment: CommentModel) -> CommentModel:
        try:
            session.add(comment)
            session.flush()
            return comment
        except IntegrityError:
            raise CommentRandomException()

    def delete(self, session: Session, comment: CommentModel) -> None:
        try:
            session.delete(comment)
            session.flush()
        except IntegrityError:
            raise CommentNotFoundException()
