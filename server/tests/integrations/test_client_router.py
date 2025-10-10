from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from invoice_reader.domain.client import Client
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.api.main import app
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.repository import (
    get_client_repository,
    get_invoice_repository,
)
from invoice_reader.interfaces.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
    PagedClientResponse,
)


def create_test_get_current_user_id(user: User):
    def _test_get_current_user_id():
        return user.id_

    return _test_get_current_user_id


@pytest.fixture
def test_client(user: User):
    client = TestClient(app)
    app.dependency_overrides[get_client_repository] = lambda: InMemoryClientRepository()
    app.dependency_overrides[get_invoice_repository] = lambda: InMemoryInvoiceRepository()
    app.dependency_overrides[get_current_user_id] = create_test_get_current_user_id(user=user)
    yield client
    app.dependency_overrides.clear()


def test_add_client(test_client: TestClient, client_create: ClientCreate):
    response = test_client.post(
        "/v1/clients",
        json=client_create.model_dump(),
    )
    assert response.status_code == 201


def test_add_existing_client(
    test_client: TestClient, client_create: ClientCreate, existing_client: Client
):
    response = test_client.post("/v1/clients", json=client_create.model_dump())
    assert response.status_code == 409


def test_get_client(test_client: TestClient, existing_client: Client):
    response = test_client.get(f"/v1/clients/{existing_client.id_}")
    client_response = ClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert client_response.client_id == existing_client.id_
    assert client_response.data.client_name == existing_client.data.client_name


def test_client_with_invoices(test_client: TestClient, existing_client_with_invoices: Client):
    response = test_client.get(f"/v1/clients/{existing_client_with_invoices.id_}")
    client_response = ClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert client_response.client_id == existing_client_with_invoices.id_
    # Client has 3 invoices, each with 10000 EUR base amount
    assert client_response.total_revenue == 10000.0 * 3
    assert client_response.n_invoices == 3


def test_update_client(
    test_client: TestClient, client_update: ClientUpdate, existing_client: Client
):
    response = test_client.put(
        f"/v1/clients/{existing_client.id_}",
        json=client_update.model_dump(),
    )
    updated_client = InMemoryClientRepository().get(client_id=existing_client.id_)
    assert response.status_code == 204
    assert updated_client is not None
    assert updated_client.data.client_name == client_update.data.client_name
    assert updated_client.data.street_number == client_update.data.street_number


def test_delete_client(test_client: TestClient, existing_client: Client):
    response = test_client.delete(f"/v1/clients/{existing_client.id_}")
    assert response.status_code == 204
    deleted_client = InMemoryClientRepository().get(client_id=existing_client.id_)
    assert deleted_client is None


def test_get_paged_clients(test_client: TestClient, existing_client: Client):
    response = test_client.get("/v1/clients")
    paged_clients = PagedClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert paged_clients.total == 1
    assert paged_clients.clients[0].client_id == existing_client.id_


def test_get_client_not_found(test_client: TestClient):
    response = test_client.get(f"/v1/clients/{uuid4()}")
    assert response.status_code == 404


def test_delete_client_not_found(test_client: TestClient):
    response = test_client.delete(f"/v1/clients/{uuid4()}")
    assert response.status_code == 404
