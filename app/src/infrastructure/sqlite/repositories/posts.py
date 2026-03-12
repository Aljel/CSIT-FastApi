from typing import Type, List, Optional
from sqlalchemy.orm import Session
from src.models import Post


class PostRepository:
    def __init__(self):
        self._model: Type[Post] = Post

    def get_published(self, session: Session, limit: int = 10) -> List[Post]:
        query = (
            session.query(self._model)
            .where(self._model.is_published)
            .order_by(self._model.pub_date.desc())
            .limit(limit)
        )
        return query.all()

    def get_by_id(self, session: Session, post_id: int) -> Optional[Post]:
        return session.query(self._model).where(self._model.id == post_id).scalar()

    def get_by_author(self, session: Session, author_id: int) -> List[Post]:
        return session.query(self._model).where(self._model.author_id == author_id).all()
