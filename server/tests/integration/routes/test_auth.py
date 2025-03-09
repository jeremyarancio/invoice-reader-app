from fastapi.testclient import TestClient

from invoice_reader.app import auth
from invoice_reader.models import UserModel
from invoice_reader.repository import UserRepository
from invoice_reader.schemas import UserCreate


def test_register_user(
    api_client: TestClient,
    new_user_create: UserCreate,
    user_repository: UserRepository,
):
    response = api_client.post(
        url="/api/v1/users/signup/",
        data=new_user_create.model_dump_json(),
    )

    user = user_repository.get_user_by_email(email=new_user_create.email)

    assert response.status_code == 201
    assert user
    assert user.email == new_user_create.email
    assert auth.verify_password(
        plain_password=new_user_create.password, hashed_password=user.hashed_password
    )


def test_register_existing_user(
    api_client: TestClient,
    existing_user_create: UserCreate,
    test_existing_user: UserModel,
):
    response = api_client.post(
        url="/api/v1/users/signup/",
        data=existing_user_create.model_dump_json(),
    )
    assert response.status_code == 409


def test_user_login(
    api_client: TestClient,
    existing_user_create: UserCreate,  # Need the non hashed pwd
    test_existing_user: UserModel,
):
    response = api_client.post(
        url="/api/v1/users/signin/",
        data={
            "username": test_existing_user.email,
            "password": existing_user_create.password,
        },
    )
    payload: dict = response.json()
    assert response.status_code == 200
    assert payload.get("access_token")


def test_user_login_wrong_password(
    api_client: TestClient, test_existing_user: UserModel
):
    response = api_client.post(
        url="/api/v1/users/signin/",
        data={"username": test_existing_user.email, "password": "wrong_password"},
    )
    assert response.status_code == 401
