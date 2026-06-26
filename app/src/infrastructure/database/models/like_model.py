from datetime import datetime
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column


class PostLikeModel(Base):
    __tablename__ = "post_like"
    __table_args__ = (UniqueConstraint("post_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("blog_post.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("auth_user.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    post: Mapped["PostModel"] = relationship(back_populates="likes")
