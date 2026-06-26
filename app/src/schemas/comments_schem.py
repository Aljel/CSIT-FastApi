from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from src.schemas.image_schem import CommentImageResponse


class CommentBase(BaseModel):
    text: str = Field(description="Текст комментария")
    post_id: int


class CommentCreate(CommentBase):
    author_id: int


class CommentUpdate(BaseModel):
    text: str = Field(description="Текст комментария")


class CommentResponse(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    images: List[CommentImageResponse] = []
