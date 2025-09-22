from uuid import UUID

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.interfaces.schemas.client import ClientUpdate
from invoice_reader.services.exceptions import EntityNotFoundException, ExistingEntityException
from invoice_reader.services.interfaces.repositories import IClientRepository
from invoice_reader.services.interfaces.repositories.invoice import IInvoiceRepository


class ClientService:
    @staticmethod
    def add_client(
        user_id: UUID,
        client_data: ClientData,
        client_repository: IClientRepository,
    ) -> None:
        existing_clients = client_repository.get_all(user_id=user_id)
        if any(client.data.client_name == client_data.client_name for client in existing_clients):
            raise ExistingEntityException(message="Client with this name already exists.")
        client = Client(
            user_id=user_id,
            data=client_data,
        )
        client_repository.add(client=client)

    @staticmethod
    def get_client(
        client_id: UUID,
        client_repository: IClientRepository,
        invoice_repository: IInvoiceRepository,
    ) -> Client:
        client = client_repository.get(client_id=client_id)
        if not client:
            raise EntityNotFoundException(message=f"Client with id {client_id} not found.")
        invoices = invoice_repository.get_by_client_id(client_id=client.id_)
        client.invoices.extend(invoices)
        return client

    @staticmethod
    def get_paged_clients(
        user_id: UUID,
        client_repository: IClientRepository,
        invoice_repository: IInvoiceRepository,
        page: int,
        per_page: int,
    ) -> list[Client]:
        clients = client_repository.get_all(user_id=user_id)
        for client in clients:
            client.invoices.extend(invoice_repository.get_by_client_id(client_id=client.id_))
        start = (page - 1) * per_page
        end = start + per_page
        return clients[start:end]

    @staticmethod
    def delete_client(
        client_id: UUID,
        client_repository: IClientRepository,
    ) -> None:
        client = client_repository.get(client_id=client_id)
        if not client:
            raise EntityNotFoundException(message="Client not found. Deletion cancelled.")
        client_repository.delete(client_id=client_id)

    @staticmethod
    def update_client(
        user_id: UUID,
        client_id: UUID,
        client_update: ClientUpdate,
        client_repository: IClientRepository,
    ) -> None:
        existing_clients = client_repository.get_all(user_id=user_id)
        if not existing_clients:
            raise EntityNotFoundException(message=f"No existing clients found for user {user_id}.")
        if any(
            client.data.client_name == client_update.client_name and client.id_ != client_id
            for client in existing_clients
        ):
            raise ExistingEntityException(
                message=f"Client with name {client_update.client_name} already exists."
            )
        client = next((client for client in existing_clients if client.id_ == client_id), None)
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
