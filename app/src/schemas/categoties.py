from pydantic import BaseModel, Field
from datetime import datetime


class Category(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    description: str = Field(description='Описание')
    slug: str = Field(
        max_length=64, description='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание')
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(
        default=datetime.now(), description='Добавлено')
