import uuid
from typing import Sequence

from invoice_reader.core.stats import compute_total_revenu_per_client
from invoice_reader.models import ClientModel
from invoice_reader.schemas import client_schema


class ClientMapper:
    @staticmethod
    def map_client_model_to_client(
        client_model: ClientModel,
    ) -> client_schema.ClientPresenter:
        return client_schema.ClientPresenter(
            total_revenu=compute_total_revenu_per_client(client_model),
            **client_model.model_dump(),
        )

    @classmethod
    def map_client_models_to_clients(
        cls,
        client_models: Sequence[ClientModel],
    ) -> list[client_schema.ClientPresenter]:
        return [
            cls.map_client_model_to_client(client_model=client_model)
            for client_model in client_models
        ]

    @staticmethod
    def map_client_to_response(
        client: client_schema.ClientPresenter,
    ) -> client_schema.ClientResponse:
        return client_schema.ClientResponse.model_validate(client.model_dump())

    @classmethod
    def map_clients_to_responses(
        cls,
        clients: list[client_schema.ClientPresenter],
    ) -> list[client_schema.ClientResponse]:
        return [cls.map_client_to_response(client) for client in clients]

    @staticmethod
    def map_client_to_model(
        client: client_schema.ClientPresenter, user_id: uuid.UUID
    ) -> ClientModel:
        return ClientModel(user_id=user_id, **client.model_dump())

    @staticmethod
    def map_client_create_to_client(
        client_create: client_schema.ClientCreate,
    ) -> client_schema.ClientPresenter:
        return client_schema.ClientPresenter.model_validate(client_create.model_dump())
