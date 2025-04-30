from fastapi.testclient import TestClient

from invoice_reader.models import ClientModel, InvoiceModel, UserModel
from invoice_reader.repository import ClientRepository
from invoice_reader.schemas import AuthToken
from invoice_reader.schemas.clients import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
    PagedClientResponse,
)


def test_add_client(
    api_client: TestClient,
    new_client: ClientCreate,
    auth_token: AuthToken,
    client_repository: ClientRepository,
    test_existing_user: UserModel,
):
    response = api_client.post(
        url="/api/v1/clients/",
        json=new_client.model_dump(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )

    client = client_repository.get_by_name(
        client_name=new_client.client_name, user_id=test_existing_user.user_id
    )

    assert response.status_code == 201
    assert client
    assert client.client_name == new_client.client_name
    assert client.street_address == new_client.street_address


def test_add_existing_client(
    api_client: TestClient,
    auth_token: AuthToken,
    test_existing_client: ClientModel,
):
    response = api_client.post(
        url="/api/v1/clients/",
        data=test_existing_client.model_dump_json(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert response.status_code == 409


def test_get_client(
    auth_token: AuthToken,
    api_client: TestClient,
    test_existing_client: ClientModel,
    test_existing_invoices: list[InvoiceModel],
):
    response = api_client.get(
        url=f"/api/v1/clients/{test_existing_client.client_id}",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    client = ClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert test_existing_client.client_name == client.client_name
    assert client.total_revenu == sum(
        [invoice.amount_excluding_tax for invoice in test_existing_invoices]
    )


def test_get_clients(
    auth_token: AuthToken,
    api_client: TestClient,
    test_existing_clients: list[ClientModel],
):
    response = api_client.get(
        url="/api/v1/clients/",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    paged_clients = PagedClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert paged_clients.total == len(test_existing_clients)
    assert paged_clients.data[0].client_name == test_existing_clients[0].client_name


def test_delete_client(
    api_client: TestClient,
    test_existing_user: UserModel,
    test_existing_client: ClientModel,
    auth_token: AuthToken,
    client_repository: ClientRepository,
):
    response = api_client.delete(
        url=f"/api/v1/clients/{test_existing_client.client_id}",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    client = client_repository.get_by_name(
        client_name=test_existing_client.client_name, user_id=test_existing_user.user_id
    )
    assert response.status_code == 204
    assert not client


def test_update_client(
    api_client: TestClient,
    test_existing_client: ClientModel,
    auth_token: AuthToken,
    client_repository: ClientRepository,
):
    updated_client = ClientUpdate.model_validate(test_existing_client.model_dump())
    updated_client.client_name = "updated_client_name"

    response = api_client.put(
        url=f"/api/v1/clients/{test_existing_client.client_id}",
        json=updated_client.model_dump(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )

    client_model = client_repository.get(
        user_id=test_existing_client.user_id,
        client_id=test_existing_client.client_id,
    )
    assert response.status_code == 204
    assert client_model
    assert client_model.client_name == updated_client.client_name
