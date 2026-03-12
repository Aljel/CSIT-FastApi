from datetime import datetime
from infrastructure.sqlite.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .comments import Comment
from .users import User
from .categories import Category


class Post(Base):
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

    author: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category"] = relationship(back_populates="posts")
    comments: Mapped["Comment"] = relationship(back_populates="post")
