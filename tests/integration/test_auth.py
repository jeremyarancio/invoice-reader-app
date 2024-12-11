import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine, select

from invoice_reader import db
from invoice_reader.app import auth
from invoice_reader.app.routes import app
from invoice_reader.models import UserModel
from invoice_reader.schemas import User, UserCreate


@pytest.fixture(name="session")
def session_fixture() -> Session:  # type: ignore
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[db.get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def user():
    return UserCreate(email="jeremy@email.com", password="password")


@pytest.fixture
def existing_user():
    return User(
        user_id=uuid.uuid4(),
        email="jeremy@email.com",
        hashed_password=auth.get_password_hash("password"),
        is_disabled=False,
    )


def add_user_to_db(user: User, session: Session) -> None:
    """
    Args:
        user_id (uuid.UUID | None): Some tests require a specific user_id. Deprecated.
    """
    user_model = UserModel(**user.model_dump())
    session.add(user_model)
    session.commit()


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
