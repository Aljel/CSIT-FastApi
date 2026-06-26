import os
import uuid
from pathlib import Path
from typing import List
from fastapi import UploadFile
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.image_repo import ImageRepository
from src.infrastructure.database.repositories.posts_repo import PostRepository
from src.infrastructure.database.repositories.comments_repo import CommentRepository
from src.schemas.image_schem import PostImageResponse, CommentImageResponse
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    CommentNotFoundByIdException,
)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024
MEDIA_ROOT = Path("media")


class ImageUseCases:
    def __init__(self):
        self._database = database
        self._repo = ImageRepository()
        self._post_repo = PostRepository()
        self._comment_repo = CommentRepository()

    def _validate_file(self, file: UploadFile) -> None:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise ValueError(
                f"Неподдерживаемый тип файла: {file.content_type}. "
                f"Допустимы: {', '.join(ALLOWED_MIME_TYPES)}"
            )
        if file.size and file.size > MAX_FILE_SIZE:
            raise ValueError(
                f"Файл слишком большой: {file.size} байт "
                f"(максимум {MAX_FILE_SIZE})"
            )

    def _save_file(self, parent_type: str, parent_id: int, file: UploadFile) -> str:
        ext = os.path.splitext(file.filename or "image")[1] or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        rel_dir = f"{parent_type}s/{parent_id}"
        rel_path = f"{rel_dir}/{filename}"
        abs_dir = MEDIA_ROOT / rel_dir
        abs_dir.mkdir(parents=True, exist_ok=True)
        content = file.file.read()
        with open(MEDIA_ROOT / rel_path, "wb") as f:
            f.write(content)
        return rel_path

    def _delete_file(self, file_path: str) -> None:
        abs_path = MEDIA_ROOT / file_path
        if abs_path.exists():
            abs_path.unlink()

    def _to_post_image_response(self, img) -> PostImageResponse:
        return PostImageResponse(
            id=img.id,
            url=f"/api/v1/media/{img.file_path}",
            file_name=img.file_name,
            file_size=img.file_size,
            mime_type=img.mime_type,
            sort_order=img.sort_order,
            created_at=img.created_at,
        )

    def _to_comment_image_response(self, img) -> CommentImageResponse:
        return CommentImageResponse(
            id=img.id,
            url=f"/api/v1/media/{img.file_path}",
            file_name=img.file_name,
            file_size=img.file_size,
            mime_type=img.mime_type,
            sort_order=img.sort_order,
            created_at=img.created_at,
        )

    def upload_post_images(
        self, post_id: int, files: List[UploadFile], user_id: int
    ) -> list[PostImageResponse]:
        with self._database.session() as session:
            post = self._post_repo.get_by_id(session, post_id)
            if post is None:
                raise PostNotFoundByIdException(id=post_id)
            if post.author_id != user_id:
                raise PermissionError(
                    "Только автор поста может загружать изображения"
                )

            existing = self._repo.get_post_images(session, post_id)
            sort_base = len(existing)
            results = []
            for i, file in enumerate(files):
                self._validate_file(file)
                rel_path = self._save_file("post", post_id, file)
                img = self._repo.create_post_image(
                    session,
                    post_id,
                    rel_path,
                    file.filename or "image",
                    file.size or 0,
                    file.content_type or "image/jpeg",
                    sort_order=sort_base + i,
                )
                results.append(self._to_post_image_response(img))
            return results

    def get_post_images(self, post_id: int) -> list[PostImageResponse]:
        with self._database.session() as session:
            imgs = self._repo.get_post_images(session, post_id)
            return [self._to_post_image_response(img) for img in imgs]

    def delete_post_image(self, image_id: int, user_id: int) -> None:
        with self._database.session() as session:
            img = self._repo.get_post_image_by_id(session, image_id)
            if img is None:
                return
            post = self._post_repo.get_by_id(session, img.post_id)
            if post is None or post.author_id != user_id:
                raise PermissionError(
                    "Только автор поста может удалять изображения"
                )
            self._delete_file(img.file_path)
            self._repo.delete_post_image(session, img)

    def upload_comment_images(
        self, comment_id: int, files: List[UploadFile], user_id: int
    ) -> list[CommentImageResponse]:
        with self._database.session() as session:
            comment = self._comment_repo.get_by_id(session, comment_id)
            if comment is None:
                raise CommentNotFoundByIdException(id=comment_id)
            if comment.author_id != user_id:
                raise PermissionError(
                    "Только автор комментария может загружать изображения"
                )

            results = []
            for i, file in enumerate(files):
                self._validate_file(file)
                rel_path = self._save_file("comment", comment_id, file)
                img = self._repo.create_comment_image(
                    session,
                    comment_id,
                    rel_path,
                    file.filename or "image",
                    file.size or 0,
                    file.content_type or "image/jpeg",
                    sort_order=i,
                )
                results.append(self._to_comment_image_response(img))
            return results

    def get_comment_images(self, comment_id: int) -> list[CommentImageResponse]:
        with self._database.session() as session:
            imgs = self._repo.get_comment_images(session, comment_id)
            return [self._to_comment_image_response(img) for img in imgs]

    def delete_comment_image(self, image_id: int, user_id: int) -> None:
        with self._database.session() as session:
            img = self._repo.get_comment_image_by_id(session, image_id)
            if img is None:
                return
            comment = self._comment_repo.get_by_id(session, img.comment_id)
            if comment is None or comment.author_id != user_id:
                raise PermissionError(
                    "Только автор комментария может удалять изображения"
                )
            self._delete_file(img.file_path)
            self._repo.delete_comment_image(session, img)


