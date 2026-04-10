from typing import Type, List, Optional
from sqlalchemy.exc import IntegrityError
from src.core.exceptions.database_exceptions import PostNotFoundException, PostAlreadyExistsException, PostRandomException
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.posts_model import PostModel


class PostRepository:
    def __init__(self):
        self._model: Type[PostModel] = PostModel

    def get_by_id(self, session: Session, post_id: int) -> Optional[PostModel]:
        try:
            return session.query(self._model).filter(self._model.id == post_id).first()
        except IntegrityError:
            raise PostNotFoundException()

    def get_published(self, session: Session, limit: int = 10) -> List[PostModel]:
        try:
            return (session.query(self._model)
                    .filter(self._model.is_published == True)
                    .order_by(self._model.pub_date.desc())
                    .limit(limit).all())
        except IntegrityError:
            raise PostRandomException()

    def create(self, session: Session, post: PostModel) -> PostModel:
        try:
            session.add(post)
            session.flush()
            return post
        except IntegrityError:
            raise PostAlreadyExistsException()

    def delete(self, session: Session, post: PostModel) -> None:
        try:
            session.delete(post)
            session.flush()
        except IntegrityError:
            raise PostNotFoundException()
