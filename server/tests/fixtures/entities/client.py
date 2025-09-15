import pytest

from invoice_reader.domain.client import Client, ClientBase, ClientUpdate
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.interfaces.schemas.client import ClientCreate

TOTAL_NUMBER = 3


@pytest.fixture
def client_base() -> ClientBase:
    return ClientBase(
        client_name="Test Client",  # NOTE: Exact name used in test_parser to match client_id with client_name when parsed
        street_number=123,
        street_address="Test St",
        city="Test City",
        country="Test Country",
        zipcode="12345",
    )


@pytest.fixture
def client(user: User, client_base: ClientBase) -> Client:
    return Client(user_id=user.id_, **client_base.model_dump())


@pytest.fixture
def existing_client(client: Client):
    InMemoryClientRepository().add(client)
    return client


@pytest.fixture
def client_create(client_base: ClientBase) -> ClientCreate:
    return ClientCreate(**client_base.model_dump())


@pytest.fixture
def client_update(client_base: ClientBase) -> ClientUpdate:
    client_base.client_name = "Updated Client Name"
    client_base.street_number = 456
    return ClientUpdate.model_validate(client_base.model_dump())
