from fastapi import HTTPException
from datetime import datetime
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.comments_repo import CommentRepository
from src.infrastructure.sqlite.models.comments_model import CommentModel
from src.schemas.comments_schem import CommentCreate, CommentResponse
from src.core.exceptions.database_exceptions import PostNotFoundException, CommentNotFoundException, CommentRandomException
from src.core.exceptions.domain_exceptions import PostNotFoundByIdException, CommentNotFoundByIdException, CommentMemeException


class CommentUseCases:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def create(self, data: CommentCreate) -> CommentResponse:
        try:
            with self._database.session() as session:
                comment = CommentModel(
                    text=data.text,
                    post_id=data.post_id,
                    author_id=data.author_id,
                    created_at=datetime.now()
                )
                created = self._repo.create(session, comment)
                return CommentResponse.model_validate(created, from_attributes=True)
        except CommentRandomException:
            raise CommentMemeException()

    async def get_by_post(self, post_id: int) -> List[CommentResponse]:
        try:
            with self._database.session() as session:
                comments = self._repo.get_by_post_id(session, post_id)
                if comments is None:
                    raise CommentMemeException()
                return [CommentResponse.model_validate(c, from_attributes=True) for c in comments]
        except PostNotFoundException:
            raise PostNotFoundByIdException(id=post_id)

    async def delete(self, comment_id: int) -> None:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if comment is None:
                    raise CommentNotFoundByIdException(id=comment_id)
                self._repo.delete(session, comment)
                session.commit()
        except CommentRandomException:
            raise CommentMemeException()
