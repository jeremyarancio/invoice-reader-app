import pytest

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.domain.invoice import Invoice
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.interfaces.schemas.client import ClientCreate, ClientUpdate


@pytest.fixture
def client_data() -> ClientData:
    return ClientData(
        client_name="Test Client",  # NOTE: match client_id with client_name when parsed
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
def client_with_invoices(client: Client, invoice: Invoice) -> Client:
    client_copy = client.model_copy(deep=True)
    client_copy.invoices.extend([invoice for _ in range(3)])
    return client_copy


@pytest.fixture
def existing_client(client: Client):
    InMemoryClientRepository().add(client)
    return client


@pytest.fixture
def existing_client_with_invoices(client_with_invoices: Client):
    InMemoryClientRepository().add(client_with_invoices)
    return client_with_invoices


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
    return ClientUpdate(
        data=client_data.model_copy(
            update={
                "client_name": "Updated Client Name",
                "street_number": 456,
            },
            deep=True,
        )
    )
