import uuid
from typing import Sequence

from invoice_reader.core.stats import compute_total_revenu_per_client
from invoice_reader.models import ClientModel
from invoice_reader.schemas.clients import Client, ClientCreate, ClientResponse


class ClientMapper:
    @staticmethod
    def map_client_model_to_client(
        client_model: ClientModel,
    ) -> Client:
        return Client(
            total_revenu=compute_total_revenu_per_client(client_model),
            **client_model.model_dump(),
        )

    @classmethod
    def map_client_models_to_clients(
        cls,
        client_models: Sequence[ClientModel],
    ) -> list[Client]:
        return [
            cls.map_client_model_to_client(client_model=client_model)
            for client_model in client_models
        ]

    @staticmethod
    def map_client_to_response(
        client: Client,
    ) -> ClientResponse:
        return ClientResponse.model_validate(client.model_dump())

    @classmethod
    def map_clients_to_responses(
        cls,
        clients: list[Client],
    ) -> list[ClientResponse]:
        return [cls.map_client_to_response(client) for client in clients]

    @staticmethod
    def map_client_to_model(client: Client, user_id: uuid.UUID) -> ClientModel:
        return ClientModel(user_id=user_id, **client.model_dump())

    @staticmethod
    def map_client_create_to_client(
        client_create: ClientCreate,
    ) -> Client:
        return Client.model_validate(client_create.model_dump())
