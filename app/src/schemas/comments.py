from pydantic import BaseModel, Field
from datetime import datetime


class CommentBase(BaseModel):
    text: str = Field(description='Текст комментария')
    post_id: int


class CommentCreate(CommentBase):
    author_id: int


class CommentResponse(CommentBase):
    id: int
    author_id: int
    created_at: datetime
