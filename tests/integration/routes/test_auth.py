from fastapi.testclient import TestClient

from invoice_reader.app import auth
from invoice_reader.models import UserModel
from invoice_reader.schemas import UserCreate


def test_register_user(
    api_client: TestClient, user_create: UserCreate, test_user: UserModel
):
    response = api_client.post(
        url="/api/v1/users/register/",
        json=user_create.model_dump(),
    )
    assert response.status_code == 200
    assert user_model is not None
    assert user_model.email == user_create.email
    assert auth.verify_password(user_create.password, user_model.hashed_password)


def test_register_existing_user(api_client: TestClient, user_create: UserCreate):
    response = api_client.post(
        url="/api/v1/users/register/",
        json=user_create.model_dump(),
    )
    assert response.status_code == 409


def test_user_login(api_client: TestClient, user_create: UserCreate):
    response = api_client.post(
        url="/api/v1/users/login/",
        data={"username": user_create.email, "password": user_create.password},
    )
    payload: dict = response.json()
    assert response.status_code == 200
    assert payload.get("access_token")
