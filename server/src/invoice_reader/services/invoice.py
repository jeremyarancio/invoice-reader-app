from uuid import UUID
from typing import BinaryIO

from invoice_reader import settings
from invoice_reader.domain import InvoiceData, Invoice, File, InvoiceID
from invoice_reader.services.interfaces.repositories import (
    IInvoiceRepository,
    IFileRepository,
)
from invoice_reader.services.exceptions import (
    ExistingEntityException,
    RollbackException,
    EntityNotFoundException,
)
from invoice_reader.utils.logger import get_logger


logger = get_logger()


class InvoiceService:
    @classmethod
    def upload_invoice(
        cls,
        file_bin: BinaryIO,
        filename: str,
        user_id: UUID,
        client_id: UUID,
        invoice_data: InvoiceData,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
    ) -> None:
        existing_invoice = invoice_repository.get_by_invoice_number(
            user_id=user_id,
            invoice_number=invoice_data.invoice_number,
        )
        if existing_invoice:
            raise ExistingEntityException(
                message="Invoice with this number already exists."
            )
        storage_path = file_repository.create_storage_path(filename=filename)
        file = File(
            file=file_bin,
            filename=filename,
            storage_path=storage_path,
        )
        invoice = Invoice(
            user_id=user_id,
            client_id=client_id,
            file=file,
            data=invoice_data,
        )
        try:
            file_repository.store(file=file)
            invoice_repository.add(invoice=invoice)
        except Exception as err:
            cls._rollback_upload(
                invoice=invoice,
                invoice_repository=invoice_repository,
                file_repository=file_repository,
                error=err,
            )

    @staticmethod
    def _rollback_upload(
        invoice: Invoice,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
        error: Exception,
    ) -> None:
        try:
            file_repository.delete(file=invoice.file)
            invoice_repository.delete(invoice_id=invoice.id_)
            raise RollbackException(
                message=f"Invoice not properly uploaded. Rollback successful. Error: {error}"
            )
        except Exception as e:
            raise RollbackException(message=f"Rollback failed. Error: {e}") from e

    @staticmethod
    def _rollback_deletion(
        invoice: Invoice,
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
        error: Exception,
    ) -> None:
        try:
            invoice_repository.add(invoice=invoice)
            file_repository.store(file=invoice.file)
            raise RollbackException(
                message=f"Invoice not properly deleted. Rollback successful. Error: {error}"
            )
        except Exception as e:
            raise RollbackException(
                message=f"Rollback failed. Error: {e}. Check invoice id {invoice.id_} and file storage path {invoice.file.storage_path} if nothing is missing."
            ) from e

    @staticmethod
    def get_invoice(
        invoice_id: InvoiceID, invoice_repository: IInvoiceRepository
    ) -> Invoice:
        invoice = invoice_repository.get(invoice_id=invoice_id)
        if invoice:
            return invoice
        else:
            raise EntityNotFoundException(
                message=f"Invoice with id {invoice_id} not found."
            )

    @staticmethod
    def get_paged_invoices(
        user_id: UUID, invoice_repository: IInvoiceRepository, page: int, per_page: int
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
        try:
            # DB
            invoice = invoice_repository.get(invoice_id=invoice_id)
            if not invoice:
                raise EntityNotFoundException(
                    message="Invoice not found. Deletion cancelled."
                )
            invoice_repository.delete(invoice_id=invoice_id)
            # Storage
            file_repository.delete(file=invoice.file)
        except Exception as e:
            cls._rollback_deletion(
                invoice=invoice,  # NOTE: Potentially an issue here!
                invoice_repository=invoice_repository,
                file_repository=file_repository,
                error=e,
            )

    @staticmethod
    def update_invoice(
        user_id: UUID,
        invoice_id: InvoiceID,
        client_id: UUID,
        invoice_data: InvoiceData,
        invoice_repository: IInvoiceRepository,
    ) -> None:
        # Check for duplicate invoice numbers (excluding the current invoice)
        existing_invoices = invoice_repository.get_all(user_id=user_id)
        if not existing_invoices:
            raise EntityNotFoundException(
                message=f"No existing invoices found for user {user_id}."
            )
        if any(
            invoice.data.invoice_number == invoice_data.invoice_number
            and invoice.id_ != invoice_id
            for invoice in existing_invoices
        ):
            raise ExistingEntityException(
                message=f"Invoice with number {invoice_data.invoice_number} already exists."
            )

        # Update invoice
        invoice = invoice_repository.get(invoice_id=invoice_id)
        invoice_repository.update(
            invoice=invoice,
            values_to_update=InvoiceMapper.map_invoice_update_for_model(
                invoice_update=invoice_update
            ),
        )

    def get_invoice_url(
        invoice_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
    ) -> str:
        if not settings.S3_BUCKET_NAME:
            raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
        s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
        invoice_repository = InvoiceRepository(session=session)
        invoice_model = invoice_repository.get(file_id=invoice_id, user_id=user_id)
        if not invoice_model:
            raise INVOICE_NOT_FOUND
        invoice = InvoiceMapper.map_invoice_model_to_invoice(
            invoice_model=invoice_model
        )
        if not invoice.s3_path:
            raise ValueError(f"s3_path of invoice {invoice_id} not found.")
        suffix = s3_utils.get_suffix_from_s3_path(s3_path=invoice.s3_path)
        url = s3.create_presigned_url(suffix=suffix)
        return url

    def extract_invoice(
        file: BinaryIO,
    ) -> InvoiceExtraction:
        return parse_invoice(file)
