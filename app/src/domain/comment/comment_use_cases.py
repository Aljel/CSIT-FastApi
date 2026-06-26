import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.comments_repo import CommentRepository
from src.infrastructure.database.models.comments_model import CommentModel
from src.schemas.comments_schem import CommentCreate, CommentUpdate, CommentResponse
from src.schemas.image_schem import CommentImageResponse
from src.core.exceptions.database_exceptions import (
    CommentNotFoundException,
    CommentRandomException,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    CommentMemeException,
)

logger = logging.getLogger(__name__)


class CommentUseCases:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    def _build_images(self, comment: CommentModel) -> list[CommentImageResponse]:
        if not comment.images:
            return []
        return [
            CommentImageResponse(
                id=img.id,
                url=f"/api/v1/media/{img.file_path}",
                file_name=img.file_name,
                file_size=img.file_size,
                mime_type=img.mime_type,
                sort_order=img.sort_order,
                created_at=img.created_at,
            )
            for img in comment.images
        ]

    async def create(self, data: CommentCreate) -> CommentResponse:
        try:
            with self._database.session() as session:
                comment = CommentModel(
                    text=data.text,
                    post_id=data.post_id,
                    author_id=data.author_id,
                    created_at=datetime.now(),
                )
                created = self._repo.create(session, comment)
                logger.info(f"Комментарий успешно добавлен (ID: {created.id})")
                resp = CommentResponse.model_validate(created, from_attributes=True)
                resp.images = self._build_images(created)
                return resp
        except CommentRandomException:
            logger.error(f"Ошибка при создании комментария: {
                         CommentRandomException}")
            raise CommentMemeException()

    async def get_by_post(self, post_id: int) -> List[CommentResponse]:
        with self._database.session() as session:
            comments = self._repo.get_by_post_id(session, post_id)
            result = []
            for c in comments:
                resp = CommentResponse.model_validate(c, from_attributes=True)
                resp.images = self._build_images(c)
                result.append(resp)
            return result

    async def update(self, comment_id: int, data: CommentUpdate) -> CommentResponse:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if comment is None:
                    raise CommentNotFoundByIdException(id=comment_id)
                updated = self._repo.update(session, comment, data.model_dump())
                logger.info(f"Комментарий ID {comment_id} обновлен")
                resp = CommentResponse.model_validate(updated, from_attributes=True)
                resp.images = self._build_images(updated)
                return resp
        except CommentRandomException:
            raise CommentMemeException()

    async def get_by_id(self, comment_id: int) -> CommentResponse:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if comment is None:
                    raise CommentNotFoundByIdException(id=comment_id)
                resp = CommentResponse.model_validate(comment, from_attributes=True)
                resp.images = self._build_images(comment)
                return resp
        except CommentRandomException:
            raise CommentMemeException()

    async def delete(self, comment_id: int) -> None:
        try:
            with self._database.session() as session:
                comment = self._repo.get_by_id(session, comment_id)
                if comment is None:
                    raise CommentNotFoundByIdException(id=comment_id)
                self._repo.delete(session, comment)
                logger.info(f"Комментарий ID {comment_id} успешно удален")
        except CommentNotFoundException:
            logger.error(f"Комментарий с ID {comment_id} не найден")
            raise CommentNotFoundByIdException(id=comment_id)
        else:
            img_dir = Path("media") / f"comments/{comment_id}"
            if img_dir.exists():
                shutil.rmtree(img_dir)
