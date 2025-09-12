from uuid import uuid4

import pytest
from sqlmodel import Session

from invoice_reader.domain.client import Client
from invoice_reader.infrastructure.repositories.client import SQLModelClientRepository


@pytest.fixture
def repository(session: Session) -> SQLModelClientRepository:
    return SQLModelClientRepository(session)


@pytest.fixture
def client() -> Client:
    return Client(
        user_id=uuid4(),
        client_name="Test Client",
        city="Test City",
        country="Test Country",
        street_address="123 Main St",
        street_number=123,
        zipcode="12345",
    )


def test_add_and_get_client(repository: SQLModelClientRepository, client: Client):
    repository.add(client)
    result = repository.get(client_id=client.id_)
    assert result is not None
    assert result.client_name == client.client_name
    assert result.user_id == client.user_id


def test_get_all_clients(repository: SQLModelClientRepository, client: Client):
    repository.add(client)
    clients = repository.get_all(user_id=client.user_id)
    assert len(clients) == 1
    for client in clients:
        assert client.client_name == client.client_name


def test_get_by_name(repository: SQLModelClientRepository, client: Client):
    repository.add(client)
    result = repository.get_by_name(client_name=client.client_name, user_id=client.user_id)
    assert result is not None
    assert result.id_ == client.id_


def test_update_client(repository: SQLModelClientRepository, client: Client):
    repository.add(client)
    client.street_address = "456 New Address"
    repository.update(client)
    updated = repository.get(client.id_)
    assert updated is not None
    assert updated.street_address == "456 New Address"


def test_delete_client(repository: SQLModelClientRepository, client: Client):
    repository.add(client)
    repository.delete(client.id_)
    result = repository.get(client.id_)
    assert result is None
