import logging
from datetime import datetime
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.posts_repo import PostRepository
from src.infrastructure.database.repositories.like_repo import LikeRepository
from src.infrastructure.database.models.posts_model import PostModel
from src.infrastructure.database.models.like_model import PostLikeModel
from src.schemas.posts_schem import PostCreate, PostUpdate, PostResponse
from typing import List, Optional as Opt
from src.core.exceptions.database_exceptions import PostAlreadyExistsException, PostRandomException, PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNameIsNotUniqueException, PostNotFoundByIdException, PostMemeException

logger = logging.getLogger(__name__)


class PostUseCases:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._like_repo = LikeRepository()

    async def create(self, data: PostCreate) -> PostResponse:
        try:
            with self._database.session() as session:
                post = PostModel(**data.model_dump())
                created = self._repo.create(session, post)
                logger.info(f"Пост создан успешно (ID: {created.id})")
                resp = PostResponse.model_validate(created, from_attributes=True)
                resp.likes_count = 0
                return resp
        except PostAlreadyExistsException:
            logger.warning(f"Пост с названием '{data.title}' уже существует")
            raise PostNameIsNotUniqueException(
                name=data.title)

    async def get_all(self, limit: int = 10, user_id: Opt[int] = None) -> List[PostResponse]:
        try:
            with self._database.session() as session:
                posts = self._repo.get_published(session, limit=limit)
                liked_ids = self._like_repo.get_user_liked_ids(
                    session, user_id) if user_id else []
                result = []
                for p in posts:
                    resp = PostResponse.model_validate(p, from_attributes=True)
                    resp.likes_count = len(p.likes) if p.likes else 0
                    resp.is_liked = p.id in liked_ids
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
                    like = self._like_repo.get_by_post_user(
                        session, post_id, user_id)
                    resp.is_liked = like is not None
                return resp
        except PostNotFoundException:
            logger.error(f"Пост с ID {post_id} не найден")
            raise PostNotFoundByIdException(id=post_id)

    async def update(self, post_id: int, data: PostUpdate, user_id: Opt[int] = None) -> PostResponse:
        update_data = data.model_dump(exclude_unset=True)
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)

                if "is_liked" in update_data and user_id is not None:
                    is_liked = update_data.pop("is_liked")
                    like = self._like_repo.get_by_post_user(
                        session, post_id, user_id)
                    if is_liked and not like:
                        session.add(PostLikeModel(
                            post_id=post_id,
                            user_id=user_id,
                            created_at=datetime.now()
                        ))
                    elif not is_liked and like:
                        session.delete(like)

                updated = self._repo.update(session, post, update_data)
                logger.info(f"Пост ID {post_id} обновлен")
                resp = PostResponse.model_validate(updated, from_attributes=True)
                resp.likes_count = len(updated.likes) if updated.likes else 0
                if user_id:
                    like = self._like_repo.get_by_post_user(
                        session, post_id, user_id)
                    resp.is_liked = like is not None
                return resp
        except PostNotFoundException:
            raise PostNotFoundByIdException(id=post_id)
        except PostAlreadyExistsException:
            raise PostNameIsNotUniqueException(
                name=data.title or "")

    async def delete(self, post_id: int) -> None:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)
                self._repo.delete(session, post)
                logger.info(f"Пост ID {post_id} успешно удален")
        except PostNotFoundException:
            logger.error(f"Пост с ID {post_id} не найден")
            raise PostNotFoundByIdException(id=post_id)
