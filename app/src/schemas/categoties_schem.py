from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    title: str = Field(max_length=256, description="Заголовок")
    description: str = Field(description="Описание")
    slug: str = Field(max_length=64)
    is_published: bool = Field(default=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=256, description="Заголовок")
    description: Optional[str] = Field(None, description="Описание")
    slug: Optional[str] = Field(None, max_length=64)
    is_published: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
