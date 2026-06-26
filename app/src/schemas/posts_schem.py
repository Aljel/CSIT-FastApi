from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from src.schemas.image_schem import PostImageResponse


class PostBase(BaseModel):
    title: str = Field(max_length=256, description="Заголовок")
    text: str = Field(description="Текст")
    pub_date: datetime
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: bool = Field(default=True)
    image_url: Optional[str] = None


class PostCreate(PostBase):
    author_id: int


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256, description="Заголовок")
    text: Optional[str] = Field(None, description="Текст")
    pub_date: Optional[datetime] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None
    image_url: Optional[str] = None


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    likes_count: int = 0
    is_liked: bool = False
    images: List[PostImageResponse] = []
