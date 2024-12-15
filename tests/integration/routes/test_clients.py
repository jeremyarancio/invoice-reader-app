
def test_add_client(
    client: TestClient,
    client_data: Client,
    auth_token: AuthToken,
    user: User,
    session: Session,
):
    response = client.post(
        url="/api/v1/clients/add/",
        json=client_data.model_dump(),
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    client_data_from_db = session.exec(
        select(ClientModel).where(ClientModel.user_id == user.user_id)
    ).first()

    assert response.status_code == 200
    assert client_data_from_db
    assert client_data_from_db.client_name == client_data.client_name


def test_add_existing_client(
    client: TestClient,
    auth_token: AuthToken,
    session: Session,
    client_models: list[ClientModel],
    user: User,
):
    client_model = client_models[0]
    session.refresh(
        client_model
    )  # Since added to the database, the object is now empty.
    client_data = Client.model_validate(client_model.model_dump())
    response = client.post(
        url="/api/v1/clients/add/",
        json=client_data.model_dump(exclude="client_id"),
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    assert response.status_code == 409


def test_get_clients(
    client_models: list[ClientModel],
    auth_token: AuthToken,
    client: TestClient,
):
    response = client.get(
        url="/api/v1/clients/",
        headers={"Authorization": f"Bearer {auth_token.access_token}"},
    )
    payload = PagedClientResponse.model_validate(response.json())
    assert response.status_code == 200
    assert payload.total == len(client_models)
