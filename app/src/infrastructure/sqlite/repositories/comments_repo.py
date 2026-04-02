from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.comments_model import CommentModel


class CommentRepository:
    def __init__(self):
        self._model: Type[CommentModel] = CommentModel

    def get_by_id(self, session: Session, comment_id: int) -> Optional[CommentModel]:
        return session.query(self._model).filter(self._model.id == comment_id).first()

    def get_by_post_id(self, session: Session, post_id: int) -> List[CommentModel]:
        return (session.query(self._model)
                .filter(self._model.post_id == post_id)
                .order_by(self._model.created_at.asc()).all())

    def create(self, session: Session, comment: CommentModel) -> CommentModel:
        session.add(comment)
        session.flush()
        return comment

    def update(self, session: Session, comment: CommentModel, update_data: dict) -> CommentModel:
        for key, value in update_data.items():
            setattr(comment, key, value)
        session.flush()
        return comment

    def delete(self, session: Session, comment: CommentModel) -> None:
        session.delete(comment)
        session.flush()
