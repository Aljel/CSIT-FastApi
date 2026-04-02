from src.domain.user.use_cases import UserUseCases
from src.domain.post.use_cases import PostUseCases
from src.domain.comment.use_cases import CommentUseCases
from src.domain.category.use_cases import CategoryUseCases


def user_use_cases() -> UserUseCases:
    return UserUseCases()


def post_use_cases() -> PostUseCases:
    return PostUseCases()


def comment_use_cases() -> CommentUseCases:
    return CommentUseCases()


def category_use_cases() -> CategoryUseCases:
    return CategoryUseCases()
