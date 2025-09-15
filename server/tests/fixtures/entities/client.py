import pytest

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.interfaces.schemas.client import ClientCreate, ClientUpdate

TOTAL_NUMBER = 3


@pytest.fixture
def client_data() -> ClientData:
    return ClientData(
        client_name="Test Client",  # NOTE: Exact name used in test_parser to match client_id with client_name when parsed
        street_number=123,
        street_address="Test St",
        city="Test City",
        country="Test Country",
        zipcode="12345",
    )


@pytest.fixture
def client(user: User, client_data: ClientData) -> Client:
    return Client(
        user_id=user.id_,
        data=client_data,
    )


@pytest.fixture
def existing_client(client: Client):
    InMemoryClientRepository().add(client)
    return client


@pytest.fixture
def client_create(client_data: ClientData) -> ClientCreate:
    return ClientCreate(
        city=client_data.city,
        client_name=client_data.client_name,
        country=client_data.country,
        street_address=client_data.street_address,
        street_number=client_data.street_number,
        zipcode=client_data.zipcode,
    )


@pytest.fixture
def client_update(client_data: ClientData) -> ClientUpdate:
    client_data.client_name = "Updated Client Name"
    client_data.street_number = 456
    return ClientUpdate.model_validate(client_data.model_dump())
