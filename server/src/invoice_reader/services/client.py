from uuid import UUID

from invoice_reader.domain.clients import BaseClient, Client, ClientID, ClientUpdate
from invoice_reader.services.exceptions import EntityNotFoundException, ExistingEntityException
from invoice_reader.services.interfaces.repositories import IClientRepository


class ClientService:
    @staticmethod
    def add_client(
        user_id: UUID,
        client_data: BaseClient,
        client_repository: IClientRepository,
    ) -> None:
        existing_clients = client_repository.get_all(user_id=user_id)
        if any(client.client_name == client_data.client_name for client in existing_clients):
            raise ExistingEntityException(message="Client with this name already exists.")
        client = Client(
            user_id=user_id,
            client_name=client_data.client_name,
            street_number=client_data.street_number,
            street_address=client_data.street_address,
            zipcode=client_data.zipcode,
            city=client_data.city,
            country=client_data.country,
        )
        client_repository.add(client=client)

    @staticmethod
    def get_client(
        client_id: ClientID,
        client_repository: IClientRepository,
    ) -> Client:
        client = client_repository.get(client_id=client_id)
        if not client:
            raise EntityNotFoundException(message=f"Client with id {client_id} not found.")
        return client

    @staticmethod
    def get_paged_clients(
        user_id: UUID,
        client_repository: IClientRepository,
        page: int,
        per_page: int,
    ) -> list[Client]:
        clients = client_repository.get_all(user_id=user_id)
        start = (page - 1) * per_page
        end = start + per_page
        return clients[start:end]

    @staticmethod
    def delete_client(
        client_id: ClientID,
        client_repository: IClientRepository,
    ) -> None:
        client = client_repository.get(client_id=client_id)
        if not client:
            raise EntityNotFoundException(message="Client not found. Deletion cancelled.")
        client_repository.delete(client_id=client_id)

    @staticmethod
    def update_client(
        user_id: UUID,
        client_id: ClientID,
        client_update: ClientUpdate,
        client_repository: IClientRepository,
    ) -> None:
        existing_clients = client_repository.get_all(user_id=user_id)
        if not existing_clients:
            raise EntityNotFoundException(message=f"No existing clients found for user {user_id}.")
        if any(
            client.client_name == client_update.client_name and client.client_id != client_id
            for client in existing_clients
        ):
            raise ExistingEntityException(
                message=f"Client with name {client_update.client_name} already exists."
            )
        client = next(
            (client for client in existing_clients if client.client_id == client_id), None
        )
        if not client:
            raise EntityNotFoundException(message=f"Client with id {client_id} not found.")
        updated_client = client.model_copy(
            update={
                "client_name": client_update.client_name,
                "street_number": client_update.street_number,
                "street_address": client_update.street_address,
                "zipcode": client_update.zipcode,
                "city": client_update.city,
                "country": client_update.country,
            }
        )
        client_repository.update(client=updated_client)
