import pytest

from invoice_reader.domain.client import Client, ClientBase
from invoice_reader.domain.user import User

TOTAL_NUMBER = 3


@pytest.fixture
def client_base() -> ClientBase:
    return ClientBase(
        client_name="Test Client",
        street_number=123,
        street_address="Test St",
        city="Test City",
        country="Test Country",
        zipcode="12345",
    )


@pytest.fixture
def existing_clients_base() -> list[ClientBase]:
    return [
        ClientBase(
            client_name=f"Client {i}",
            street_number=123 + i,
            street_address=f"Test St {i}",
            city="Test City",
            country="Test Country",
            zipcode=f"1234{i}",
        )
        for i in range(TOTAL_NUMBER)
    ]


@pytest.fixture
def existing_client_base() -> ClientBase:
    return ClientBase(
        client_name="Existing Client",
        street_number=999,
        street_address="Existing St",
        city="Existing City",
        country="Existing Country",
        zipcode="99999",
    )


@pytest.fixture
def client(user: User, client_base: ClientBase) -> Client:
    return Client(user_id=user.id_, **client_base.model_dump())
