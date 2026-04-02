from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.posts_model import PostModel


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get_by_id(self, session: Session, post_id: int) -> Optional[PostModel]:
        return session.query(self._model).filter(self._model.id == post_id).first()

    def get_published(self, session: Session, limit: int = 10) -> List[PostModel]:
        return (session.query(self._model)
                .filter(self._model.is_published == True)
                .order_by(self._model.pub_date.desc())
                .limit(limit).all())

    def create(self, session: Session, post: PostModel) -> PostModel:
        session.add(post)
        session.flush()
        return post

    def update(self, session: Session, post: PostModel, update_data: dict) -> PostModel:
        for key, value in update_data.items():
            setattr(post, key, value)
        session.flush()
        return post

    def delete(self, session: Session, post: PostModel) -> None:
        session.delete(post)
        session.flush()
