from datetime import datetime
from src.infrastructure.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class PostImageModel(Base):
    __tablename__ = "post_image"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id", ondelete="CASCADE"))
    file_path: Mapped[str]
    file_name: Mapped[str]
    file_size: Mapped[int]
    mime_type: Mapped[str]
    sort_order: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    post: Mapped["PostModel"] = relationship(back_populates="images")
