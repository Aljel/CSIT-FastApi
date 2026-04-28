import logging
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts_repo import PostRepository
from src.infrastructure.sqlite.models.posts_model import PostModel
from src.schemas.posts_schem import PostCreate, PostResponse
from typing import List
from src.core.exceptions.database_exceptions import PostAlreadyExistsException, PostRandomException, PostNotFoundException
from src.core.exceptions.domain_exceptions import PostNameIsNotUniqueException, PostNotFoundByIdException, PostMemeException

logger = logging.getLogger(__name__)


class PostUseCases:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def create(self, data: PostCreate) -> PostResponse:
        try:
            with self._database.session() as session:
                post = PostModel(**data.model_dump())
                created = self._repo.create(session, post)
                logger.info(f"Пост создан успешно (ID: {created.id})")
                return PostResponse.model_validate(created, from_attributes=True)
        except PostAlreadyExistsException:
            logger.warning(f"Пост с названием '{data.title}' уже существует")
            raise PostNameIsNotUniqueException(
                name=data.title)

    async def get_all(self, limit: int = 10) -> List[PostResponse]:
        try:
            with self._database.session() as session:
                posts = self._repo.get_published(session, limit=limit)
                return [PostResponse.model_validate(p, from_attributes=True) for p in posts]
        except PostRandomException:
            raise PostMemeException()

    async def get_by_id(self, post_id: int) -> PostResponse:
        try:
            with self._database.session() as session:
                post = self._repo.get_by_id(session, post_id)
                if post is None:
                    raise PostNotFoundByIdException(id=post_id)
                return PostResponse.model_validate(post, from_attributes=True)
        except PostNotFoundException:
            logger.error(f"Пост с ID {post_id} не найден")
            raise PostNotFoundByIdException(id=post_id)

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
