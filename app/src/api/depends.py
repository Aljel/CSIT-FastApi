from src.domain.user.user_use_cases import UserUseCases
from src.domain.post.post_use_cases import PostUseCases
from src.domain.comment.comment_use_cases import CommentUseCases
from src.domain.category.category_use_cases import CategoryUseCases


def user_use_cases() -> UserUseCases:
    return UserUseCases()


def post_use_cases() -> PostUseCases:
    return PostUseCases()


def comment_use_cases() -> CommentUseCases:
    return CommentUseCases()


def category_use_cases() -> CategoryUseCases:
    return CategoryUseCases()
