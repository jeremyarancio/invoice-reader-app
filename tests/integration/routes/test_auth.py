from fastapi.testclient import TestClient
from sqlmodel import Session, select

from invoice_reader.app import auth
from invoice_reader.models import UserModel
from invoice_reader.schemas import User, UserCreate


def test_register_user(client: TestClient, session: Session, user: UserCreate):
    response = client.post(
        url="/api/v1/users/register/",
        json=user.model_dump(),
    )
    assert response.status_code == 200
    user_model = session.exec(select(UserModel)).first()
    assert user_model is not None
    assert user_model.email == user.email
    assert auth.verify_password(user.password, user_model.hashed_password)


def test_register_existing_user(
    client: TestClient, session: Session, user: UserCreate, existing_user: User
):
    add_user_to_db(user=existing_user, session=session)
    response = client.post(
        url="/api/v1/users/register/",
        json=user.model_dump(),
    )
    assert response.status_code == 409


def test_user_login(client: TestClient, session: Session, existing_user: User):
    add_user_to_db(user=existing_user, session=session)
    response = client.post(
        url="/api/v1/users/login/",
        data={"username": existing_user.email, "password": "password"},
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("access_token")
