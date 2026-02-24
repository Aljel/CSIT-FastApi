from pydantic import BaseModel, Field
from datetime import datetime


class Comment(BaseModel):
    text: str = Field(description='Текст комментария')
    post_id: int = Field(description='Публикация')
    created_at: datetime = Field(
        default=datetime.now(), description='Дата и время создания')
    author_id: int = Field(description='ID автора')
