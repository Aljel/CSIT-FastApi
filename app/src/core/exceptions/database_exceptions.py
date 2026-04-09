class BaseDatabaseException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseException):
    pass


class UserAlreadyExistsException(BaseDatabaseException):
    pass


class PostNotFoundException(BaseDatabaseException):
    pass


class PostAlreadyExistsException(BaseDatabaseException):
    pass


class CommentNotFoundException(BaseDatabaseException):
    pass


class CategoryNotFoundException(BaseDatabaseException):
    pass


class CategoryAlreadyExistsException(BaseDatabaseException):
    pass
