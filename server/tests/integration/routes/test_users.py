from fastapi.testclient import TestClient

from invoice_reader.schemas import AuthToken

from ..utils import assert_status_code


def test_get_user(
    api_client: TestClient,
    auth_token: AuthToken,
):
    response = api_client.get(
        url="/api/v1/users/me/",
        headers={"Authorization": f"{auth_token.token_type} {auth_token.access_token}"},
    )
    assert_status_code(response, 200)
