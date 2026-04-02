from datetime import datetime
from src.infrastructure.sqlite.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .posts_model import PostModel
from .comments_model import CommentModel


class UserModel(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_staff: Mapped[bool]
    is_active: Mapped[bool]
    is_superuser: Mapped[bool]
    last_login: Mapped[datetime]
    date_joined: Mapped[datetime]
    posts: Mapped["PostModel"] = relationship(back_populates="author")
    comments: Mapped["CommentModel"] = relationship(
        back_populates="author")
