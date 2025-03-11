from typing import Sequence

from invoice_reader.models import UserModel
from invoice_reader.schemas.users import UserCreate, UserPresenter, UserResponse


class UserMapper:
    @staticmethod
    def map_user_model_to_user(
        user_model: UserModel,
    ) -> UserPresenter:
        return UserPresenter.model_validate(user_model.model_dump())

    @classmethod
    def map_user_models_to_users(
        cls,
        client_models: Sequence[UserModel],
    ) -> list[UserPresenter]:
        return [
            cls.map_user_model_to_user(user_model=user_model)
            for user_model in client_models
        ]

    @staticmethod
    def map_user_to_response(
        user: UserPresenter,
    ) -> UserResponse:
        return UserResponse.model_validate(user.model_dump())

    @classmethod
    def map_users_to_responses(
        cls,
        users: list[UserPresenter],
    ) -> list[UserResponse]:
        return [cls.map_user_to_response(user) for user in users]

    @staticmethod
    def map_user_create_to_user(
        user_create: UserCreate,
        hashed_password: str,
        is_disable: bool = False,
    ) -> UserPresenter:
        return UserPresenter(
            hashed_password=hashed_password,
            is_disabled=is_disable,
            **user_create.model_dump(),
        )

    @staticmethod
    def map_user_to_model(user: UserPresenter) -> UserModel:
        return UserModel.model_validate(user.model_dump())
