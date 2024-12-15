import pytest
import uuid

from sqlmodel import Session, StaticPool, SQLModel, select, create_engine
from fastapi.testclient import TestClient

from invoice_reader import db
from invoice_reader.app import routes, auth
from invoice_reader.schemas import (
    UserCreate,
    User,
)


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

    routes.app.dependency_overrides[db.get_session] = get_session_override
    client = TestClient(routes.app)
    yield client
    routes.app.dependency_overrides.clear()


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



@pytest.fixture(name="session")
def session_fixture() -> Session:  # type: ignore
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def user():
    return User(
        user_id=uuid.uuid4(),
        email="jeremy@email.com",
        hashed_password=auth.get_password_hash("password"),
        is_disabled=False,
    )



@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[db.get_session] = get_session_override
    try:
        client = TestClient(app)
        yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def filepath() -> str:
    return "tests/assets/paper.pdf"


@pytest.fixture
def upload_files(filepath):
    with open(filepath, "rb") as f:
        files = {"upload_file": ("filename.pdf", f, "application/pdf")}
        yield files


@pytest.fixture
def file_data(user: User) -> FileData:
    return FileData(user_id=user.user_id, filename="filename.pdf")


@pytest.fixture
def s3_bucket() -> str:
    return "bucket"


@pytest.fixture
def s3_suffix(file_data: FileData) -> str:
    return f"{file_data.user_id}/{file_data.file_id}{file_data.file_format}"


@pytest.fixture
def s3_mocker(mocker) -> Mock:
    mock_client = Mock()
    mocker.patch("boto3.client", return_value=mock_client)
    return mock_client


@pytest.fixture
def bucket() -> str:
    return "bucket"


@pytest.fixture
def invoice_data():
    return Invoice(
        invoiced_date=datetime.date(2024, 11, 18),
        invoice_number="14SQ456",
        amount_excluding_tax=10000,
        currency="€",
        vat="20",
    )


@pytest.fixture
def client_data():
    return Client(
        client_name="Sacha&Cie",
        street_number="19",
        street_address="road of coal",
        city="Carcassone",
        country="France",
        zipcode=45777,
    )


@pytest.fixture
def auth_token(user: User) -> AuthToken:
    access_token = auth.create_access_token(email=user.email)
    return AuthToken(access_token=access_token, token_type="bearer")


@pytest.fixture
def client_id() -> str:
    return str(uuid.uuid4())



@pytest.fixture
def wrong_files(request, filepath: str):
    key, mime_type = request.param
    with open(filepath, "rb") as f:
        files = {key: (key, f, mime_type)}
        yield files


@pytest.mark.parametrize(
    "wrong_files",
    [
        ("wrong_filename", "application/json"),
        ("upload_file", "image/jpeg"),
    ],
    indirect=True,
)



@pytest.fixture
def invoice_models(
    file_data: FileData, invoice_data: Invoice, s3_suffix: str
) -> list[InvoiceModel]:
    total = 3
    invoice_models = [
        InvoiceModel(
            file_id=uuid.uuid4(),  # To respect unique primary key we update the id at each iteration
            s3_path=s3_suffix,
            user_id=file_data.user_id,
            client_id=uuid.uuid4(),
            **invoice_data.model_dump(),
        )
        for _ in range(total)
    ]
    return invoice_models


@pytest.fixture
def client_models(user: User) -> list[ClientModel]:
    return [
        ClientModel(
            user_id=user.user_id,
            client_name=f"client_{i}",
            zipcode=75000,
            city="Paris",
            country="France",
            street_address="Rivoli",
            street_number=155,
        )
        for i in range(5)
    ]