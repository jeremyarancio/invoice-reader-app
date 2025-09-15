import pytest

from invoice_reader.domain.client import Client, ClientBase
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository

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
