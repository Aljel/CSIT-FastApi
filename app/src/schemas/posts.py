from pydantic import BaseModel, Field
from datetime import datetime


class Post(BaseModel):
    title: str = Field(max_length=256, description='Заголовок')
    text: str = Field(description='Текст')
    pub_date: datetime = Field(
        description='Дата и время публикации. Если установить дату и время в будущем - можно делать отложенные публикации')
    author_id: int = Field(description='Автор публикации')
    location_id: int = Field(default=None, description='Местоположение')
    category_id: int = Field(default=None, description='Категория')
    is_published: bool = Field(default=True, description='Опубликовано')
    created_at: datetime = Field(
        default=datetime.now(), description='Добавлено')
    image_url: str = Field(
        default=None, description='URL прикрепленного изображения')
