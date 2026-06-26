from pydantic import BaseModel


class LikeToggleRequest(BaseModel):
    post_id: int


class LikeToggleResponse(BaseModel):
    is_liked: bool
    likes_count: int
