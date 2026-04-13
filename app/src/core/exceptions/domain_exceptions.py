class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с именем='{username}' не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username)

        super().__init__(detail=self._exception_text_template)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с именем='{username}' уже существует"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username)

        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с идентификатором '{id}' не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id)

        super().__init__(detail=self._exception_text_template)


class PostNameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пост с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            name=name)

        super().__init__(detail=self._exception_text_template)


class PostMemeException(BaseDomainException):
    _exception_text_template = "skill issue"

    def __init__(self) -> None:
        self._exception_text_template = self._exception_text_template.format()

        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с идентификатором '{id}' не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            id=id)

        super().__init__(detail=self._exception_text_template)
