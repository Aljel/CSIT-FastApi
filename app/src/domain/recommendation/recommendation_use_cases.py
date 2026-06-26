import numpy as np
from typing import Optional
from src.infrastructure.database.database import database
from src.infrastructure.database.repositories.posts_repo import PostRepository
from src.infrastructure.database.repositories.like_repo import LikeRepository
from src.infrastructure.database.repositories.embedding_repo import EmbeddingRepository
from src.schemas.posts_schem import PostResponse


class RecommendationUseCases:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._like_repo = LikeRepository()
        self._embedding_repo = EmbeddingRepository()

    async def get_similar(
        self, post_id: int, limit: int = 5, user_id: Optional[int] = None
    ) -> list[PostResponse]:
        with self._database.session() as session:
            target_emb = self._embedding_repo.get_by_post_id(session, post_id)
            if target_emb is None:
                return []
            target_vec = np.array(target_emb.embedding["vec"])

            embeddings = self._embedding_repo.get_all(session)
            liked_ids = (
                set(self._like_repo.get_user_liked_ids(session, user_id))
                if user_id
                else set()
            )

            scores: list[tuple[float, int]] = []
            for emb in embeddings:
                if emb.post_id == post_id:
                    continue
                vec = np.array(emb.embedding["vec"])
                sim = float(target_vec @ vec)
                scores.append((sim, emb.post_id))

            scores.sort(key=lambda x: -x[0])
            top_ids = [pid for _, pid in scores[:limit]]

            posts = self._repo.get_by_ids(session, top_ids)
            post_map = {p.id: p for p in posts}
            result = []
            for pid in top_ids:
                p = post_map.get(pid)
                if p is None:
                    continue
                resp = PostResponse.model_validate(p, from_attributes=True)
                resp.likes_count = len(p.likes) if p.likes else 0
                resp.is_liked = p.id in liked_ids
                result.append(resp)
            return result

    async def get_personalized(self, user_id: int, limit: int = 10) -> list[PostResponse]:
        with self._database.session() as session:
            liked_ids = self._like_repo.get_user_liked_ids(session, user_id)
            liked_ids_set = set(liked_ids)

            if not liked_ids:
                return await self._get_trending(session, limit, liked_ids_set)

            embeddings = self._embedding_repo.get_all(session)
            emb_by_post = {e.post_id: np.array(
                e.embedding["vec"]) for e in embeddings}

            liked_vecs = [emb_by_post[pid]
                          for pid in liked_ids if pid in emb_by_post]
            if not liked_vecs:
                return await self._get_trending(session, limit, liked_ids_set)

            user_vec = np.mean(liked_vecs, axis=0)
            user_vec = user_vec / (user_vec @ user_vec) ** 0.5

            scores: list[tuple[float, int]] = []
            for pid, vec in emb_by_post.items():
                if pid in liked_ids_set:
                    continue
                sim = float(user_vec @ vec)
                scores.append((sim, pid))

            scores.sort(key=lambda x: -x[0])
            top_ids = [pid for _, pid in scores[:limit]]

            posts = self._repo.get_by_ids(session, top_ids)
            post_map = {p.id: p for p in posts}
            result = []
            for pid in top_ids:
                p = post_map.get(pid)
                if p is None:
                    continue
                resp = PostResponse.model_validate(p, from_attributes=True)
                resp.likes_count = len(p.likes) if p.likes else 0
                resp.is_liked = p.id in liked_ids_set
                result.append(resp)
            return result

    async def get_trending(self, limit: int = 10) -> list[PostResponse]:
        with self._database.session() as session:
            return await self._get_trending(session, limit, set())

    async def _get_trending(
        self, session, limit: int, liked_ids_set: set
    ) -> list[PostResponse]:
        posts = self._repo.get_by_likes(session, limit=limit)
        result = []
        for p in posts:
            resp = PostResponse.model_validate(p, from_attributes=True)
            resp.likes_count = len(p.likes) if p.likes else 0
            resp.is_liked = p.id in liked_ids_set
            result.append(resp)
        return result
