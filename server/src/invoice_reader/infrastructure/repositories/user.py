from uuid import UUID

from sqlmodel import Session, select

from invoice_reader.domain.user import User
from invoice_reader.infrastructure.models import UserModel
from invoice_reader.services.interfaces.repositories import IUserRepository


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users: dict[UUID, User] = {}

    def add(self, user: User) -> None:
        self.users[user.id_] = user

    def get(self, user_id: UUID) -> User | None:
        return self.users.get(user_id)

    def update(self, user: User) -> None:
        if user.id_ in self.users:
            self.users[user.id_] = user

    def delete(self, user_id: UUID) -> None:
        if user_id in self.users:
            self.users.pop(user_id)

    def get_all(self) -> list[User]:
        return list(self.users.values())

    def get_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user


class SQLModelUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_model(self, user: User) -> UserModel:
        """Convert domain entity to infrastructure model."""
        return UserModel(
            user_id=user.id_,
            email=user.email,
            hashed_password=user.hashed_password,
            is_disabled=user.is_disabled,
        )

    def _to_entity(self, model: UserModel) -> User:
        """Convert infrastructure model to domain entity."""
        return User(
            id_=model.user_id,
            email=model.email,
            hashed_password=model.hashed_password,
            is_disabled=model.is_disabled,
        )

    def add(self, user: User) -> None:
        user_model = self._to_model(user)
        self.session.add(user_model)
        self.session.commit()

    def update(self, user: User) -> None:
        existing_user_model = self.session.exec(
            select(UserModel).where(UserModel.user_id == user.id_)
        ).one()

        # Update existing model with new values
        updated_data = self._to_model(user).model_dump(exclude={"id"})  # Assuming SQLModel
        for key, value in updated_data.items():
            setattr(existing_user_model, key, value)

        self.session.add(existing_user_model)
        self.session.commit()

    def get(self, user_id: UUID) -> User | None:
        user_model = self.session.exec(
            select(UserModel).where(UserModel.user_id == user_id)
        ).one_or_none()
        return self._to_entity(user_model) if user_model else None

    def delete(self, user_id: UUID) -> None:
        user_model = self.session.exec(select(UserModel).where(UserModel.user_id == user_id)).one()
        self.session.delete(user_model)
        self.session.commit()

    def get_all(self) -> list[User]:
        user_models = self.session.exec(select(UserModel)).all()
        return [self._to_entity(model) for model in user_models]

    def get_by_email(self, email: str) -> User | None:
        user_model = self.session.exec(
            select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        return self._to_entity(user_model) if user_model else None
