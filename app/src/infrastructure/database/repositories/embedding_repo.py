from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.models.embedding_model import PostEmbeddingModel


class EmbeddingRepository:
    def get_by_post_id(
        self, session: Session, post_id: int
    ) -> Optional[PostEmbeddingModel]:
        return (
            session.query(PostEmbeddingModel)
            .filter(PostEmbeddingModel.post_id == post_id)
            .first()
        )

    def get_all(self, session: Session) -> list[PostEmbeddingModel]:
        return session.query(PostEmbeddingModel).all()

    def save(
        self, session: Session, post_id: int, embedding: list[float]
    ) -> PostEmbeddingModel:
        existing = self.get_by_post_id(session, post_id)
        if existing:
            existing.embedding = {"vec": embedding}
            return existing
        model = PostEmbeddingModel(
            post_id=post_id,
            embedding={"vec": embedding},
        )
        session.add(model)
        return model

    def delete_by_post_id(self, session: Session, post_id: int) -> None:
        session.query(PostEmbeddingModel).filter(
            PostEmbeddingModel.post_id == post_id
        ).delete()
