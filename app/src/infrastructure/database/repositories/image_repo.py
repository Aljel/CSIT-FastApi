from typing import Optional
from sqlalchemy.orm import Session
from src.infrastructure.database.models.post_image_model import PostImageModel
from src.infrastructure.database.models.comment_image_model import CommentImageModel


class ImageRepository:
    def create_post_image(
        self,
        session: Session,
        post_id: int,
        file_path: str,
        file_name: str,
        file_size: int,
        mime_type: str,
        sort_order: int = 0,
    ) -> PostImageModel:
        model = PostImageModel(
            post_id=post_id,
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            sort_order=sort_order,
        )
        session.add(model)
        session.flush()
        return model

    def get_post_images(self, session: Session, post_id: int) -> list[PostImageModel]:
        return (
            session.query(PostImageModel)
            .filter(PostImageModel.post_id == post_id)
            .order_by(PostImageModel.sort_order)
            .all()
        )

    def get_post_image_by_id(
        self, session: Session, image_id: int
    ) -> Optional[PostImageModel]:
        return (
            session.query(PostImageModel)
            .filter(PostImageModel.id == image_id)
            .first()
        )

    def delete_post_image(self, session: Session, image: PostImageModel) -> None:
        session.delete(image)

    def create_comment_image(
        self,
        session: Session,
        comment_id: int,
        file_path: str,
        file_name: str,
        file_size: int,
        mime_type: str,
        sort_order: int = 0,
    ) -> CommentImageModel:
        model = CommentImageModel(
            comment_id=comment_id,
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            mime_type=mime_type,
            sort_order=sort_order,
        )
        session.add(model)
        session.flush()
        return model

    def get_comment_images(
        self, session: Session, comment_id: int
    ) -> list[CommentImageModel]:
        return (
            session.query(CommentImageModel)
            .filter(CommentImageModel.comment_id == comment_id)
            .order_by(CommentImageModel.sort_order)
            .all()
        )

    def get_comment_image_by_id(
        self, session: Session, image_id: int
    ) -> Optional[CommentImageModel]:
        return (
            session.query(CommentImageModel)
            .filter(CommentImageModel.id == image_id)
            .first()
        )

    def delete_comment_image(
        self, session: Session, image: CommentImageModel
    ) -> None:
        session.delete(image)
