from datetime import datetime
from infrastructure.sqlite.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .posts import Post
from .users import User


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime]
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id"))
    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"))

    post: Mapped["Post"] = relationship(back_populates="comments")
    author: Mapped["User"] = relationship(back_populates="comments")
