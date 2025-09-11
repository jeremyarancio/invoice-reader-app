import pytest

from invoice_reader.schemas.clients import Client

TOTAL_NUMBER = 3


@pytest.fixture
def new_client():
    return Client(
        client_name="Sacha&Cie",
        street_number=19,
        street_address="road of coal",
        city="Carcassone",
        country="France",
        zipcode=45777,
    )


@pytest.fixture
def existing_client():
    return Client(
        client_name="Steren",
        street_number=19,
        street_address="road of coal",
        city="Carcassone",
        country="France",
        zipcode=45777,
    )


@pytest.fixture
def existing_clients() -> list[Client]:
    return [
        Client(
            client_name=f"client-{i}",
            street_number=19,
            street_address="road of coal",
            city="Carcassone",
            country="France",
            zipcode=45777,
        )
        for i in range(TOTAL_NUMBER)
    ]
