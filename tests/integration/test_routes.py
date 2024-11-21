from unittest.mock import Mock
import datetime
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool, select

from invoice_reader.app.routes import app
from invoice_reader import db
from invoice_reader import models  # noqa: F401
from invoice_reader.schemas import (
	InvoiceSchema,
	FileData,
	UserSchema,
)
from invoice_reader.models import UserModel
from invoice_reader import settings


@pytest.fixture(name="session")
def session_fixture() -> Session:  # type: ignore
	engine = create_engine(
		"sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
	)
	SQLModel.metadata.create_all(engine)
	with Session(engine) as session:
		yield session


def add_user_to_db(user: UserSchema, user_id: uuid.UUID, session: Session) -> uuid.UUID:
	user_model = UserModel(user_id=user_id, **user.model_dump())
	session.add(user_model)
	session.commit()
	return user_model.user_id


@pytest.fixture(name="client")
def client_fixture(session: Session):
	def get_session_override():
		return session

	app.dependency_overrides[db.get_session] = get_session_override
	client = TestClient(app)
	yield client
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
def file_data() -> FileData:
	return FileData(user_id=settings._USER_ID, filename="filename.pdf")


@pytest.fixture
def s3_bucket() -> str:
	return settings.S3_BUCKET


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
	return InvoiceSchema(
		client_name="Sacha&Cie",
		invoiced_date=datetime.date(2024, 11, 18),
		invoice_number="14SQ456",
		street_number="19",
		street_address="road of coal",
		city="Carcassone",
		country="France",
		zipcode=45777,
		amount_excluding_tax=10000,
		currency="€",
		vat="20",
	)


def test_submit_invoice(
	upload_files,
	client: TestClient,
	s3_mocker: Mock,
	invoice_data: InvoiceSchema,
	session: Session,
):
	data = invoice_data.model_dump_json()
	response = client.post(url="api/v1/files/submit/", data={"data": data}, files=upload_files)
	user_id = add_user_to_db(
		user=UserSchema(email="jeremy@hotmail.com"),
		user_id=settings._USER_ID,
		session=session,
	)
	invoice_data_from_db = session.exec(
		select(models.InvoiceModel).where(models.InvoiceModel.user_id == user_id)
	).one_or_none()

	assert invoice_data_from_db is not None
	assert response.status_code == 200
	s3_mocker.upload_fileobj.assert_called_once()
	assert invoice_data_from_db.city == invoice_data.city
	assert invoice_data_from_db.country == invoice_data.country
	assert invoice_data_from_db.client_name == invoice_data.client_name
	assert invoice_data_from_db.street_address == invoice_data.street_address
	assert invoice_data_from_db.street_number == invoice_data.street_number
	assert invoice_data_from_db.amount_excluding_tax == invoice_data.amount_excluding_tax
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
def test_submit_invoice_with_wrong_format(wrong_files, client: TestClient, s3_mocker: Mock):
	response = client.post(url="api/v1/files/submit/", files=wrong_files)
	assert response.status_code == 422
	s3_mocker.assert_not_called()


@pytest.fixture
def user() -> UserSchema:
	return UserSchema(email="jeremy@email.com")


def test_register_user(client: TestClient, session: Session, user: UserSchema):
	response = client.post(
		url="/api/v1/users/register/",
		json=user.model_dump(),
	)
	assert response.status_code == 200
	user_model = session.exec(select(UserModel)).first()
	assert user_model is not None
	assert user_model.email == user.email
