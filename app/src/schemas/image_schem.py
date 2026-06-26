from pydantic import BaseModel
from datetime import datetime


class PostImageResponse(BaseModel):
    id: int
    url: str = ""
    file_name: str
    file_size: int
    mime_type: str
    sort_order: int
    created_at: datetime


class CommentImageResponse(BaseModel):
    id: int
    url: str = ""
    file_name: str
    file_size: int
    mime_type: str
    sort_order: int
    created_at: datetime
