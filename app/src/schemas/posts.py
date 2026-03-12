from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: bool = Field(default=True)
    image_url: Optional[str] = None


class PostCreate(PostBase):
    # author_id обычно берется из токена авторизации, но пока оставим тут
    author_id: int


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
