from fastapi.testclient import TestClient

from invoice_reader.schemas import AuthToken, Client, PagedClientGetResponse
from invoice_reader.models import ClientModel, UserModel
from invoice_reader.repository import ClientRepository


def test_add_client(
    api_client: TestClient,
    new_client: Client,
    auth_token: AuthToken,
    client_repository: ClientRepository,
    test_existing_user: UserModel,
):
    response = api_client.post(
        url="/api/v1/clients/add/",
        data=new_client.model_dump_json(),
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
    test_existing_user: UserModel,
    test_existing_client: ClientModel,
):
    response = api_client.post(
        url="/api/v1/clients/add/",
        data=test_existing_client.model_dump_json(),
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert response.status_code == 409


def test_get_clients(
    auth_token: AuthToken,
    api_client: TestClient,
    test_existing_clients: list[ClientModel],
    test_existing_user: UserModel,
):
    response = api_client.get(
        url="/api/v1/clients/",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    paged_clients = PagedClientGetResponse.model_validate(response.json())
    assert response.status_code == 200
    assert paged_clients.total == len(test_existing_clients)
    assert paged_clients.data[0].client_name == test_existing_clients[0].client_name
