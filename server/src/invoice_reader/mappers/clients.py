import uuid
from typing import Sequence

from invoice_reader.core.stats import compute_total_revenu_per_client
from invoice_reader.models import ClientModel
from invoice_reader.schemas.clients import (
    Client,
    ClientCreate,
    ClientResponse,
    ClientUpdate,
)


class ClientMapper:
    @staticmethod
    def map_client_model_to_client(
        client_model: ClientModel,
    ) -> Client:
        return Client(
            client_id=client_model.client_id,
            client_name=client_model.client_name,
            zipcode=client_model.zipcode,
            city=client_model.city,
            country=client_model.country,
            street_number=client_model.street_number,
            street_address=client_model.street_address,
            total_revenu=compute_total_revenu_per_client(client_model),
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

    @staticmethod
    def map_client_update_to_client(client_update: ClientUpdate) -> Client:
        return Client.model_validate(client_update.model_dump())

    @staticmethod
    def map_client_update_for_model(client_update: ClientUpdate) -> dict:
        return {
            "client_name": client_update.client_name,
            "zipcode": client_update.zipcode,
            "city": client_update.city,
            "country": client_update.country,
            "street_number": client_update.street_number,
            "street_address": client_update.street_address,
        }
