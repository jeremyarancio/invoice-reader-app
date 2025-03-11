from typing import Sequence

from invoice_reader.models import UserModel
from invoice_reader.schemas import user_schema


class UserMapper:
    @staticmethod
    def map_user_model_to_user(
        user_model: UserModel,
    ) -> user_schema.UserPresenter:
        return user_schema.UserPresenter.model_validate(user_model.model_dump())

    @classmethod
    def map_user_models_to_users(
        cls,
        client_models: Sequence[UserModel],
    ) -> list[user_schema.UserPresenter]:
        return [
            cls.map_user_model_to_user(user_model=user_model)
            for user_model in client_models
        ]

    @staticmethod
    def map_user_to_response(
        user: user_schema.UserPresenter,
    ) -> user_schema.UserResponse:
        return user_schema.UserResponse.model_validate(user.model_dump())

    @classmethod
    def map_users_to_responses(
        cls,
        users: list[user_schema.UserPresenter],
    ) -> list[user_schema.UserResponse]:
        return [cls.map_user_to_response(user) for user in users]

    @staticmethod
    def map_user_create_to_user(
        user_create: user_schema.UserCreate,
        hashed_password: str,
        is_disable: bool = False,
    ) -> user_schema.UserPresenter:
        return user_schema.UserPresenter(
            hashed_password=hashed_password,
            is_disabled=is_disable,
            **user_create.model_dump(),
        )

    @staticmethod
    def map_user_to_model(user: user_schema.UserPresenter) -> UserModel:
        return UserModel.model_validate(user.model_dump())
