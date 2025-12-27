from uuid import UUID

from invoice_reader.domain.client import Client, ClientData
from invoice_reader.domain.invoice import Currency
from invoice_reader.services.exceptions import (
    EntityNotFoundException,
    ExistingEntityException,
)
from invoice_reader.services.exchange_rates import get_exchange_rate
from invoice_reader.services.interfaces.exchange_rates import IExchangeRateService
from invoice_reader.services.interfaces.repositories import IClientRepository
from invoice_reader.services.interfaces.repositories.exchange_rate import IExchangeRateRepository
from invoice_reader.services.interfaces.repositories.invoice import IInvoiceRepository
from invoice_reader.utils.logger import get_logger

logger = get_logger()


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
        client_update_data: ClientData,
        client_repository: IClientRepository,
    ) -> None:
        existing_clients = client_repository.get_all(user_id=user_id)
        if not existing_clients:
            raise EntityNotFoundException(message=f"No existing clients found for user {user_id}.")
        if any(
            client.data.client_name == client_update_data.client_name and client.id_ != client_id
            for client in existing_clients
        ):
            raise ExistingEntityException(
                message=f"Client with name {client_update_data.client_name} already exists."
            )
        client = next((client for client in existing_clients if client.id_ == client_id), None)
        if not client:
            raise EntityNotFoundException(message=f"Client with id {client_id} not found.")
        updated_client = Client(
            id_=client.id_,
            user_id=client.user_id,
            data=client_update_data,
        )
        client_repository.update(client=updated_client)

    @classmethod
    def calculate_total_revenue(
        cls,
        client_id: UUID,
        invoice_repository: IInvoiceRepository,
        exchange_rate_service: IExchangeRateService,
        exchange_rate_repository: IExchangeRateRepository,
    ) -> dict[Currency, float] | None:
        logger.info("Calculating total revenue for client: {}", client_id)
        total_revenue = {currency: 0.0 for currency in Currency}
        invoices = invoice_repository.get_by_client_id(client_id=client_id)
        exchange_rates = get_exchange_rate(
            exchange_rate_repository=exchange_rate_repository,
            exchange_rate_service=exchange_rate_service,
        )
        # Convert each invoice to all currencies and accumulate
        for invoice in invoices:
            for target_currency in Currency:
                converted_amount = exchange_rates.convert(
                    value=invoice.data.gross_amount,
                    from_currency=invoice.data.currency,
                    to_currency=target_currency,
                )
                total_revenue[target_currency] += converted_amount

        return total_revenue

    @staticmethod
    def count_invoices(
        client_id: UUID,
        invoice_repository: IInvoiceRepository,
    ) -> int:
        invoices = invoice_repository.get_by_client_id(client_id=client_id)
        return len(invoices)
