from datetime import datetime
from src.infrastructure.sqlite.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .comments_model import CommentModel
# from .users import UserModel
from .categories_model import CategoryModel


class PostModel(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    text: Mapped[str]
    pub_date: Mapped[datetime]
    is_published: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    image_url: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))
    category_id: Mapped[int] = mapped_column(
        ForeignKey("blog_category.id"))
    location_id: Mapped[int] = mapped_column(nullable=True)

    author: Mapped["UserModel"] = relationship(back_populates="posts")
    category: Mapped["CategoryModel"] = relationship(back_populates="posts")
    comments: Mapped["CommentModel"] = relationship(back_populates="post")
