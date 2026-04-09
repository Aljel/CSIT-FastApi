from fastapi import HTTPException, status
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from src.infrastructure.sqlite.models.posts_model import PostModel
from src.schemas.posts_schem import PostCreate, PostResponse
from typing import List


class PostUseCases:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def create(self, data: PostCreate) -> PostResponse:
        with self._database.session() as session:
            post = PostModel(**data.model_dump())
            created = self._repo.create(session, post)
            return PostResponse.model_validate(created, from_attributes=True)

    async def get_all(self, limit: int = 10) -> List[PostResponse]:
        with self._database.session() as session:
            posts = self._repo.get_published(session, limit=limit)
            return [PostResponse.model_validate(p, from_attributes=True) for p in posts]

    async def get_by_id(self, post_id: int) -> PostResponse:
        with self._database.session() as session:
            post = self._repo.get_by_id(session, post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            return PostResponse.model_validate(post, from_attributes=True)

    async def update(self, post_id: int, data: dict) -> PostResponse:
        with self._database.session() as session:
            post = self._repo.get_by_id(session, post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            updated = self._repo.update(session, post, data)
            return PostResponse.model_validate(updated, from_attributes=True)

    async def delete(self, post_id: int) -> None:
        with self._database.session() as session:
            post = self._repo.get_by_id(session, post_id)
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")
            self._repo.delete(session, post)
