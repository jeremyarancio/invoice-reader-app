import pytest
from sqlmodel import Session

from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.user import SQLModelUserRepository


@pytest.fixture
def repository(session: Session) -> SQLModelUserRepository:
    return SQLModelUserRepository(session)


@pytest.fixture
def user() -> User:
    return User(
        email="testuser@example.com",
        hashed_password="hashedpassword123",
        is_disabled=False,
    )


def test_add_and_get_user(repository: SQLModelUserRepository, user: User):
    repository.add(user)
    result = repository.get(user_id=user.id_)
    assert result is not None
    assert result.email == user.email
    assert result.hashed_password == user.hashed_password
    assert result.is_disabled == user.is_disabled


def test_get_all_users(repository: SQLModelUserRepository, user: User):
    repository.add(user=user)
    users = repository.get_all()
    assert len(users) == 1
    assert users[0].email == user.email


def test_get_by_email(repository: SQLModelUserRepository, user: User):
    repository.add(user=user)
    result = repository.get_by_email(email=user.email)
    assert result is not None
    assert result.id_ == user.id_


def test_update_user(repository: SQLModelUserRepository, user: User):
    repository.add(user=user)
    user.is_disabled = True
    repository.update(user=user)
    updated = repository.get(user_id=user.id_)
    assert updated is not None
    assert updated.is_disabled is True


def test_delete_user(repository: SQLModelUserRepository, user: User):
    repository.add(user)
    repository.delete(user.id_)
    result = repository.get(user.id_)
    assert result is None
