from uuid import UUID

from sqlmodel import Session, select

from invoice_reader.domain.user import User
from invoice_reader.infrastructure.models import UserModel
from invoice_reader.services.interfaces.repositories import IUserRepository


class SQLModelUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        user_model = UserModel(
            user_id=user.id_,
            email=user.email,
            hashed_password=user.hashed_password,
            is_disabled=user.is_disabled,
        )
        self.session.add(user_model)
        self.session.commit()

    def update(self, user: User) -> None:
        existing_user_model = self.session.exec(
            select(UserModel).where(UserModel.user_id == user.id_)
        ).one()
        user_model = UserModel(
            user_id=user.id_,
            email=user.email,
            hashed_password=user.hashed_password,
            is_disabled=user.is_disabled,
        )
        updated_user_model = existing_user_model.sqlmodel_update(user_model)
        self.session.add(updated_user_model)
        self.session.commit()

    def get(self, user_id: UUID) -> User | None:
        user_model = self.session.exec(
            select(UserModel).where(UserModel.user_id == user_id)
        ).one_or_none()
        if user_model:
            return User(
                id_=user_model.user_id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                is_disabled=user_model.is_disabled,
            )

    def delete(self, user_id: UUID) -> None:
        user_model = self.session.exec(select(UserModel).where(UserModel.user_id == user_id)).one()
        self.session.delete(user_model)
        self.session.commit()

    def get_all(self) -> list[User]:
        user_models = self.session.exec(select(UserModel)).all()
        return [
            User(
                id_=user_model.user_id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                is_disabled=user_model.is_disabled,
            )
            for user_model in user_models
        ]

    def get_by_email(self, email: str) -> User | None:
        user_model = self.session.exec(
            select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        if user_model:
            return User(
                id_=user_model.user_id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                is_disabled=user_model.is_disabled,
            )
