import logging
import shutil
from pathlib import Path
from sqlalchemy import text
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.posts_repo import PostRepository
from src.infrastructure.database.repositories.like_repo import LikeRepository
from src.infrastructure.database.repositories.embedding_repo import EmbeddingRepository
from src.infrastructure.database.models.posts_model import PostModel
from src.infrastructure.nlp.encoder import BertEncoder
from src.schemas.posts_schem import PostCreate, PostUpdate, PostResponse
from src.schemas.image_schem import PostImageResponse
from typing import List, Optional as Opt
from src.core.exceptions.database_exceptions import (
    PostAlreadyExistsException,
    PostRandomException,
    PostNotFoundException,
)
from src.core.exceptions.domain_exceptions import (
    PostNameIsNotUniqueException,
    PostNotFoundByIdException,
    PostMemeException,
)

logger = logging.getLogger(__name__)


class PostUseCases:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._like_repo = LikeRepository()
        self._embedding_repo = EmbeddingRepository()

    def _build_images(self, post: PostModel) -> list[PostImageResponse]:
        if not post.images:
            return []
        return [
            PostImageResponse(
                id=img.id,
                url=f"/api/v1/media/{img.file_path}",
                file_name=img.file_name,
                file_size=img.file_size,
                mime_type=img.mime_type,
                sort_order=img.sort_order,
                created_at=img.created_at,
            )
            for img in post.images
        ]

    async def create(self, data: PostCreate) -> PostResponse:
        text = f"{data.title} {data.text}"
        embedding = BertEncoder.get_instance().encode(text)
        try:
            with self._database.session() as session:
                post = PostModel(**data.model_dump())
                created = self._repo.create(session, post)
                self._embedding_repo.save(session, created.id, embedding)
                logger.info(f"Пост создан успешно (ID: {created.id})")
                resp = PostResponse.model_validate(created, from_attributes=True)
                resp.likes_count = 0
                resp.images = self._build_images(created)
                return resp
        except PostAlreadyExistsException:
            logger.warning(f"Пост с названием '{data.title}' уже существует")
            raise PostNameIsNotUniqueException(name=data.title)

    async def get_all(
        self, limit: int = 10, user_id: Opt[int] = None
    ) -> List[PostResponse]:
        try:
            with self._database.session() as session:
                posts = self._repo.get_published(session, limit=limit)
                liked_ids = (
                    self._like_repo.get_user_liked_ids(session, user_id)
                    if user_id
                    else []
                )
                result = []
                for p in posts:
                    resp = PostResponse.model_validate(p, from_attributes=True)
                    resp.likes_count = len(p.likes) if p.likes else 0
                    resp.is_liked = p.id in liked_ids
                    resp.images = self._build_images(p)
                    result.append(resp)
                return result
        except PostRandomException:
            raise PostMemeException()

    async def get_by_id(self, post_id: int, user_id: Opt[int] = None) -> PostResponse:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)
                resp = PostResponse.model_validate(post, from_attributes=True)
                resp.likes_count = len(post.likes) if post.likes else 0
                if user_id:
                    like = self._like_repo.get_by_post_user(session, post_id, user_id)
                    resp.is_liked = like is not None
                resp.images = self._build_images(post)
                return resp
        except PostNotFoundException:
            logger.error(f"Пост с ID {post_id} не найден")
            raise PostNotFoundByIdException(id=post_id)

    async def update(
        self, post_id: int, data: PostUpdate, user_id: Opt[int] = None
    ) -> PostResponse:
        update_data = data.model_dump(exclude_unset=True)
        needs_reembed = "title" in update_data or "text" in update_data
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)

                updated = self._repo.update(session, post, update_data)

                if needs_reembed:
                    text = f"{updated.title} {updated.text}"
                    embedding = BertEncoder.get_instance().encode(text)
                    self._embedding_repo.save(session, post_id, embedding)

                logger.info(f"Пост ID {post_id} обновлен")
                resp = PostResponse.model_validate(updated, from_attributes=True)
                resp.likes_count = len(updated.likes) if updated.likes else 0
                if user_id:
                    like = self._like_repo.get_by_post_user(session, post_id, user_id)
                    resp.is_liked = like is not None
                resp.images = self._build_images(updated)
                return resp
        except PostNotFoundException:
            raise PostNotFoundByIdException(id=post_id)
        except PostAlreadyExistsException:
            raise PostNameIsNotUniqueException(name=data.title or "")

    async def delete(self, post_id: int) -> None:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)

                comment_ids = [row[0] for row in session.execute(
                    text("SELECT id FROM blog_comment WHERE post_id = :pid"),
                    {"pid": post_id}
                ).fetchall()]

                self._repo.delete(session, post)
                logger.info(f"Пост ID {post_id} успешно удален")
        except PostNotFoundException:
            logger.error(f"Пост с ID {post_id} не найден")
            raise PostNotFoundByIdException(id=post_id)
        else:
            dirs = [Path("media") / f"posts/{post_id}"] + [Path("media") / f"comments/{cid}" for cid in comment_ids]
            for d in dirs:
                if d.exists():
                    shutil.rmtree(d)
