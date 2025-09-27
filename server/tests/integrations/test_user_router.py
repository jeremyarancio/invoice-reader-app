import pytest
from fastapi.testclient import TestClient

from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.user import InMemoryUserRepository
from invoice_reader.interfaces.api.main import app
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.repository import get_user_repository
from invoice_reader.interfaces.schemas.auth import AuthToken
from invoice_reader.interfaces.schemas.user import UserCreate
from invoice_reader.services.auth import AuthService


@pytest.fixture
def test_client(user: User):
    client = TestClient(app)
    app.dependency_overrides[get_user_repository] = lambda: InMemoryUserRepository()
    app.dependency_overrides[get_current_user_id] = lambda: user.id_
    yield client
    app.dependency_overrides.clear()


def test_register_user(test_client: TestClient, user_create: UserCreate):
    response = test_client.post("/v1/users/signup/", json=user_create.model_dump())
    assert response.status_code == 201
    user = InMemoryUserRepository().get_by_email(user_create.email)
    assert user
    assert user.email == user_create.email


def test_register_existing_user(
    test_client: TestClient, user_create: UserCreate, existing_user: User
):
    response = test_client.post("/v1/users/signup/", json=user_create.model_dump())
    assert response.status_code == 409


def test_user_login(test_client: TestClient, auth_form: dict[str, str], existing_user: User):
    response = test_client.post("/v1/users/signin/", data=auth_form)
    assert response.status_code == 200
    auth_token = AuthToken.model_validate(response.json())
    assert auth_token.token_type == "bearer"
    decoded = AuthService.decode_token(auth_token.access_token)
    assert decoded.email == existing_user.email


def test_user_login_wrong_password(test_client: TestClient, existing_user: User):
    response = test_client.post(
        "/v1/users/signin/", data={"username": existing_user.email, "password": "wrong_password"}
    )
    assert response.status_code == 401
