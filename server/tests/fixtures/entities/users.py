import uuid

import pytest

from invoice_reader.app import auth
from invoice_reader.schemas.users import User, UserCreate


@pytest.fixture
def new_user_create() -> UserCreate:
    return UserCreate(email="jeremy@email.com", password="password")


@pytest.fixture
def existing_user_create() -> UserCreate:
    return UserCreate(email="kevin@email.com", password="password")


@pytest.fixture
def existing_user(existing_user_create: UserCreate):
    return User(
        user_id=uuid.uuid4(),
        email=existing_user_create.email,
        hashed_password=auth.get_password_hash(existing_user_create.password),
        is_disabled=False,
    )
