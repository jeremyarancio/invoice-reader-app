import datetime
import uuid
from unittest.mock import Mock
import json

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine, select

from invoice_reader import (
    db,
    models,  # noqa: F401
)
from invoice_reader.app import auth
from invoice_reader.app.routes import app
from invoice_reader.models import InvoiceModel, UserModel, ClientModel
from invoice_reader.schemas import (
    AuthToken,
    FileData,
    Invoice,
    InvoiceCreate,
    InvoiceResponse,
    PagedInvoiceResponse,
    User,
    Client,
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


def add_user_to_db(user: User, session: Session) -> None:
    """
    Args:
        user_id (uuid.UUID | None): Some tests require a specific user_id. Deprecated.
    """
    user_model = UserModel(**user.model_dump())
    session.add(user_model)
    session.commit()


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
    access_token = auth.create_access_token(username=user.email)
    return AuthToken(access_token=access_token, token_type="bearer")


@pytest.fixture
def client_id() -> str:
    return str(uuid.uuid4())


def test_submit_invoice(
    upload_files,
    client: TestClient,
    s3_mocker: Mock,
    invoice_data: InvoiceCreate,
    session: Session,
    user: User,
    auth_token: AuthToken,
    client_id: str,
):
    add_user_to_db(user=user, session=session)
    data = json.dumps(
        {
            "invoice": json.loads(
                invoice_data.model_dump_json()
            ),  # Workaround because date not JSON serializable
            "client_id": client_id,
        }
    )
    response = client.post(
        url="/api/v1/files/submit",
        data={"data": data},
        files=upload_files,
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    invoice_data_from_db = session.exec(
        select(models.InvoiceModel).where(models.InvoiceModel.user_id == user.user_id)
    ).one_or_none()

    assert response.status_code == 200
    assert invoice_data_from_db is not None
    s3_mocker.upload_fileobj.assert_called_once()
    assert (
        invoice_data_from_db.amount_excluding_tax == invoice_data.amount_excluding_tax
    )
    assert invoice_data_from_db.invoice_number == invoice_data.invoice_number
    assert invoice_data_from_db.invoiced_date == invoice_data.invoiced_date
    assert invoice_data_from_db.uploaded_date is not None


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
def test_submit_invoice_with_wrong_format(
    wrong_files,
    client: TestClient,
    s3_mocker: Mock,
    auth_token: AuthToken,
):
    response = client.post(
        url="/api/v1/files/submit",
        files=wrong_files,
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    assert response.status_code == 422
    s3_mocker.assert_not_called()


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


def add_invoices_to_db(invoice_models: list[InvoiceModel], session: Session) -> None:
    session.add_all(invoice_models)
    session.commit()


def test_get_invoice(
    client: TestClient,
    auth_token: AuthToken,
    user: User,
    invoice_models: list[InvoiceModel],
    session: Session,
):
    invoice_model = invoice_models[0]
    add_user_to_db(user=user, session=session)
    add_invoices_to_db(invoice_models=[invoice_model], session=session)
    response = client.get(
        url=f"/api/v1/files/{invoice_model.file_id}",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    payload = InvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert payload.file_id == invoice_model.file_id
    assert payload.s3_path == invoice_model.s3_path
    assert payload.data.invoice_number == invoice_model.invoice_number


def test_get_invoices(
    client: TestClient,
    auth_token: AuthToken,
    user: User,
    invoice_models: list[InvoiceModel],
    session: Session,
):
    PAGE = 1
    PER_PAGE = 2
    add_user_to_db(user=user, session=session)
    add_invoices_to_db(invoice_models=invoice_models, session=session)
    response = client.get(
        url="/api/v1/files/",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
        params={"page": PAGE, "per_page": PER_PAGE},
    )
    payload = PagedInvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert len(payload.data) == PER_PAGE
    assert payload.total == len(invoice_models)
    assert all(item.data.invoice_number for item in payload.data)


def test_add_client(
    client: TestClient,
    client_data: Client,
    auth_token: AuthToken,
    user: User,
    session: Session,
):
    add_user_to_db(user=user, session=session)
    response = client.post(
        url="/api/v1/clients/add/",
        json=client_data.model_dump(),
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    client_data_from_db = session.exec(
        select(ClientModel).where(ClientModel.user_id == user.user_id)
    ).first()

    assert response.status_code == 200
    assert client_data_from_db
    assert client_data_from_db.client_name == client_data.client_name
