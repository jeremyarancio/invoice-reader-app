from typing import BinaryIO

from invoice_reader.domain.client import Client, ClientID
from invoice_reader.domain.invoice import File, Invoice, InvoiceBase, InvoiceID, InvoiceUpdate
from invoice_reader.domain.parser import ParsedInvoiceData
from invoice_reader.domain.user import UserID
from invoice_reader.services.exceptions import (
    EntityNotFoundException,
    ExistingEntityException,
    RollbackException,
)
from invoice_reader.services.interfaces.parser import IParser
from invoice_reader.services.interfaces.repositories import (
    IClientRepository,
    IFileRepository,
    IInvoiceRepository,
)
from invoice_reader.utils.logger import get_logger

logger = get_logger()


class InvoiceService:
    @classmethod
    def add_invoice(
        cls,
        file_bin: BinaryIO,
        filename: str,
        user_id: UserID,
        client_id: ClientID,
        invoice_data: InvoiceBase,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
    ) -> None:
        existing_invoice = invoice_repository.get_by_invoice_number(
            user_id=user_id,
            invoice_number=invoice_data.invoice_number,
        )
        if existing_invoice:
            raise ExistingEntityException(message="Invoice with this number already exists.")

        invoice_id = InvoiceID.create()
        initial_path = f"{user_id}/{invoice_id}.{filename.split('.')[-1]}"
        storage_path = file_repository.create_storage_path(initial_path=initial_path)
        file = File(
            file=file_bin,
            filename=filename,
            storage_path=storage_path,
        )
        invoice = Invoice(
            id_=invoice_id,
            user_id=user_id,
            client_id=client_id,
            storage_path=storage_path,
            **invoice_data.model_dump(),
        )
        try:
            file_repository.store(file=file)
            invoice_repository.add(invoice=invoice)
        except Exception as err:
            cls._rollback_add(
                invoice=invoice,
                invoice_repository=invoice_repository,
                file_repository=file_repository,
                error=err,
            )

    @staticmethod
    def _rollback_add(
        invoice: Invoice,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
        error: Exception,
    ) -> None:
        try:
            file_repository.delete(storage_path=invoice.storage_path)
            invoice_repository.delete(invoice_id=invoice.id_)
            raise RollbackException(
                message=f"Invoice not properly uploaded. Rollback successful. Error: {error}"
            )
        except Exception as e:
            raise RollbackException(message=f"Rollback failed. Error: {e}") from e

    @staticmethod
    def get_invoice(invoice_id: InvoiceID, invoice_repository: IInvoiceRepository) -> Invoice:
        invoice = invoice_repository.get(invoice_id=invoice_id)
        if invoice:
            return invoice
        else:
            raise EntityNotFoundException(message=f"Invoice with id {invoice_id} not found.")

    @staticmethod
    def get_paged_invoices(
        user_id: UserID, invoice_repository: IInvoiceRepository, page: int, per_page: int
    ) -> list[Invoice]:
        # NOTE: Can also perfom the pagination at the DB level for better performance
        invoices = invoice_repository.get_all(user_id=user_id)
        start = (page - 1) * per_page
        end = start + per_page
        return invoices[start:end]

    @classmethod
    def delete_invoice(
        cls,
        invoice_id: InvoiceID,
        invoice_repository: IInvoiceRepository,
        file_repository: IFileRepository,
    ) -> None:
        # TODO: Think about rollback
        invoice = invoice_repository.get(invoice_id=invoice_id)
        if not invoice:
            raise EntityNotFoundException(message="Invoice not found. Deletion cancelled.")
        invoice_repository.delete(invoice_id=invoice_id)
        file_repository.delete(storage_path=invoice.storage_path)

    @staticmethod
    def update_invoice(
        user_id: UserID,
        invoice_id: InvoiceID,
        invoice_update: InvoiceUpdate,
        invoice_repository: IInvoiceRepository,
    ) -> None:
        # Check for duplicate invoice numbers (excluding the current invoice)
        existing_invoices = invoice_repository.get_all(user_id=user_id)
        if not existing_invoices:
            raise EntityNotFoundException(message=f"No existing invoices found for user {user_id}.")
        if any(
            invoice.invoice_number == invoice_update.invoice_number and invoice.id_ != invoice_id
            for invoice in existing_invoices
        ):
            raise ExistingEntityException(
                message=f"Invoice with number {invoice_update.invoice_number} already exists."
            )

        # Update invoice
        invoice = next(
            (invoice for invoice in existing_invoices if invoice.id_ == invoice_id),
            None,  # Pick the invoice to update for the already fetched invoices
        )
        if not invoice:
            raise EntityNotFoundException(message=f"Invoice with id {invoice_id} not found.")
        updated_invoice = invoice.model_copy(
            update={
                "client_id": invoice_update.client_id,
                "invoice_number": invoice_update.invoice_number,
                "gross_amount": invoice_update.gross_amount,
                "vat": invoice_update.vat,
                "description": invoice_update.description,
                "issued_date": invoice_update.issued_date,
                "paid_date": invoice_update.paid_date,
                "currency": invoice_update.currency,
            }
        )
        invoice_repository.update(invoice=updated_invoice)

    @staticmethod
    def get_invoice_url(
        invoice_id: InvoiceID,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
    ) -> str:
        invoice = invoice_repository.get(invoice_id=invoice_id)
        if not invoice:
            raise EntityNotFoundException(message="Invoice not found.")
        url = file_repository.get_url(storage_path=invoice.storage_path)
        return url

    @staticmethod
    def parse_invoice(
        file: BinaryIO,
        parser: IParser,
        client_repository: IClientRepository,
        user_id: UserID,
    ) -> tuple[ParsedInvoiceData, Client | None]:
        parsed_data = parser.parse(file=file)
        client = (
            client_repository.get_by_name(
                client_name=parsed_data.client.client_name, user_id=user_id
            )
            if parsed_data.client.client_name
            else None
        )
        if not client:
            logger.warning(
                "Client with the name {} not found in the database during parsing.",
                parsed_data.client.client_name,
            )
        return parsed_data.invoice, client
