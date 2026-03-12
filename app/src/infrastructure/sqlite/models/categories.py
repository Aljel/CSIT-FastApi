from datetime import datetime
from infrastructure.sqlite.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .posts import Post


class Category(Base):
    __tablename__ = "blog_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    is_published: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    posts: Mapped["Post"] = relationship(back_populates="category")
