from src.domain.user.use_cases.get_user_by_username import GetUserByUsernameUseCase
from src.domain.user.use_cases.create_user import CreateUserUseCase


def get_user_by_username_use_case() -> GetUserByUsernameUseCase:
    return GetUserByUsernameUseCase()


def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()
