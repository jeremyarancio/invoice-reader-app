from uuid import UUID

from invoice_reader.domain.auth import EncodedToken
from invoice_reader.domain.user import User
from invoice_reader.services.auth import AuthService
from invoice_reader.services.exceptions import (
    AuthenticationException,
    EntityNotFoundException,
    ExistingEntityException,
)
from invoice_reader.services.interfaces.repositories import IUserRepository
from invoice_reader.settings import get_settings

settings = get_settings()


class UserService:
    @staticmethod
    def get_user(user_id: UUID, user_repository: IUserRepository) -> User:
        user = user_repository.get(user_id=user_id)
        if not user:
            raise EntityNotFoundException(message="User not found.")
        return user

    @staticmethod
    def register_user(email: str, password: str, user_repository: IUserRepository) -> None:
        existing_user = user_repository.get_by_email(email=email)
        if existing_user:
            raise ExistingEntityException(message="User with this email already exists.")
        hashed_password = AuthService.get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
        )
        user_repository.add(user=user)

    @staticmethod
    def authenticate_user(
        email: str,
        password: str,
        user_repository: IUserRepository,
    ) -> tuple[EncodedToken, EncodedToken]:
        user = user_repository.get_by_email(email=email)
        if not user:
            raise EntityNotFoundException(message="User not found.")
        is_valid_password = AuthService.verify_password(password, user.hashed_password)
        if not is_valid_password:
            raise AuthenticationException(message="Invalid credentials.", status_code=401)
        access_token = AuthService.create_token(
            email=user.email,
            expire=settings.access_token_expire,
            token_type="access",
        )
        refresh_token = AuthService.create_token(
            email=user.email,
            expire=settings.refresh_token_expire,
            token_type="refresh",
        )
        return access_token, refresh_token

    @staticmethod
    def delete(user_id: UUID, user_repository: IUserRepository) -> None:
        user = user_repository.get(user_id=user_id)
        if not user:
            raise EntityNotFoundException(message="User not found. Deletion cancelled.")
        user_repository.delete(user_id=user_id)
