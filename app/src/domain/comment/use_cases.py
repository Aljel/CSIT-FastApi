from fastapi import HTTPException
from datetime import datetime
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from src.infrastructure.sqlite.models.comments_model import CommentModel
from src.schemas.comments_schem import CommentCreate, CommentResponse


class CommentUseCases:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def create(self, data: CommentCreate) -> CommentResponse:
        with self._database.session() as session:
            comment = CommentModel(
                text=data.text,
                post_id=data.post_id,
                author_id=data.author_id,
                created_at=datetime.now()
            )
            created = self._repo.create(session, comment)
            return CommentResponse.model_validate(created, from_attributes=True)

    async def get_by_post(self, post_id: int) -> List[CommentResponse]:
        with self._database.session() as session:
            comments = self._repo.get_by_post_id(session, post_id)
            return [CommentResponse.model_validate(c, from_attributes=True) for c in comments]

    async def delete(self, comment_id: int) -> None:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session, comment_id)
            if not comment:
                raise HTTPException(
                    status_code=404, detail="Comment not found")
            self._repo.delete(session, comment)

    async def update(self, comment_id: int, text: str) -> CommentResponse:
        with self._database.session() as session:
            comment = self._repo.get_by_id(session, comment_id)
            if not comment:
                raise HTTPException(
                    status_code=404, detail="Comment not found")

            updated = self._repo.update(session, comment, {"text": text})
            return CommentResponse.model_validate(updated, from_attributes=True)
