from collections import defaultdict
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from invoice_reader.domain.client import Client
from invoice_reader.domain.exchange_rate import ExchangeRates
from invoice_reader.domain.invoice import Currency, Invoice
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.exchange_rates import TestExchangeRatesService
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.exchange_rate import InMemoryExchangeRateRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.api.main import app
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.exchange_rates import get_exchange_rates_service
from invoice_reader.interfaces.dependencies.repository import (
    get_client_repository,
    get_exchange_rate_repository,
    get_invoice_repository,
)
from invoice_reader.interfaces.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientRevenueResponse,
    ClientUpdate,
    PagedClientResponse,
)


@pytest.fixture
def test_client(user: User):
    client = TestClient(app)
    app.dependency_overrides[get_client_repository] = lambda: InMemoryClientRepository()
    app.dependency_overrides[get_invoice_repository] = lambda: InMemoryInvoiceRepository()
    app.dependency_overrides[get_current_user_id] = lambda: user.id_
    app.dependency_overrides[get_exchange_rates_service] = lambda: TestExchangeRatesService()
    app.dependency_overrides[get_exchange_rate_repository] = (
        lambda: InMemoryExchangeRateRepository()
    )
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


def test_calculate_total_revenue_with_no_cached_exchange_rates(
    test_client: TestClient,
    existing_client: Client,
    existing_invoices: list[Invoice],
):
    response = test_client.get(f"/v1/clients/{existing_client.id_}/revenue")
    assert response.status_code == 200
    response = ClientRevenueResponse.model_validate(response.json())

    # Calculate for the test
    exchange_rates = [
        TestExchangeRatesService().get_exchange_rates(
            base_currency=invoice.data.currency,
        )
        for invoice in existing_invoices
    ]
    converted_amounts = [
        {curr: invoice.data.gross_amount * rate}
        for invoice, ex in zip(existing_invoices, exchange_rates, strict=True)
        for curr, rate in ex.rates.items()
    ]
    total_revenue: defaultdict[Currency, float] = defaultdict(float)
    for amount in converted_amounts:
        for curr, value in amount.items():
            total_revenue[curr] += value

    assert response.total_revenue == total_revenue


def test_total_revenue_with_cached_exchange_rates(
    test_client: TestClient,
    existing_client: Client,
    existing_invoices: list[Invoice],
    existing_historical_exchange_rates: ExchangeRates,
):
    response = test_client.get(f"/v1/clients/{existing_client.id_}/revenue")
    assert response.status_code == 200
    response = ClientRevenueResponse.model_validate(response.json())

    # It works only because each invoice was issed on the same date.
    # Otherwise, each invoice would have its own exchange rates at different dates
    # prepared in fixtures
    converted_amounts = [
        {curr: invoice.data.gross_amount * rate}
        for invoice in existing_invoices
        for curr, rate in existing_historical_exchange_rates.rates.items()
    ]
    total_revenue: defaultdict[Currency, float] = defaultdict(float)
    for amount in converted_amounts:
        for curr, value in amount.items():
            total_revenue[curr] += value

    assert response.total_revenue == total_revenue


def test_count_invoices(
    test_client: TestClient,
    existing_client: Client,
    existing_invoices: list[Invoice],
):
    response = test_client.get(f"/v1/clients/{existing_client.id_}/revenue")
    assert response.status_code == 200
    response = ClientRevenueResponse.model_validate(response.json())
    assert response.n_invoices == len(existing_invoices)
