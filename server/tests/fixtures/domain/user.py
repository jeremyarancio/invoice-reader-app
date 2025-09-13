import pytest

from invoice_reader.domain.user import User


@pytest.fixture
def user() -> User:
    return User(
        email="user@example.com",
        hashed_password="securepassword",
        is_disabled=False,
    )
