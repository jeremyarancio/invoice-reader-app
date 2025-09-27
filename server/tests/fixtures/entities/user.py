import pytest

from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.user import InMemoryUserRepository
from invoice_reader.interfaces.schemas.auth import AuthToken
from invoice_reader.interfaces.schemas.user import UserCreate
from invoice_reader.services.auth import AuthService


@pytest.fixture
def user_password() -> str:
    return "securepassword"


@pytest.fixture
def user(user_password: str) -> User:
    return User(
        email="user@example.com",
        hashed_password=AuthService.get_password_hash(user_password),
        is_disabled=False,
    )


@pytest.fixture
def user_create(user: User, user_password: str) -> UserCreate:
    return UserCreate(email=user.email, password=user_password)


@pytest.fixture
def existing_user(user: User) -> User:
    InMemoryUserRepository().add(user)
    return user


@pytest.fixture
def auth_form(user: User, user_password: str) -> dict[str, str]:
    return {"username": user.email, "password": user_password}


@pytest.fixture
def auth_token(existing_user: User) -> AuthToken:
    access_token = AuthService.create_token(
        email=existing_user.email, expire=3600, token_type="access"
    )
    return AuthToken(access_token=access_token, token_type="bearer")
