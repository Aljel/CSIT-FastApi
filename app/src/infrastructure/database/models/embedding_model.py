from datetime import datetime
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column


class PostEmbeddingModel(Base):
    __tablename__ = "post_embedding"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("blog_post.id", ondelete="CASCADE"), unique=True
    )
    embedding: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
