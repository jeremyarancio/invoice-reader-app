from abc import ABC, abstractmethod
from uuid import UUID
from typing import BinaryIO

from invoice_reader import settings
from invoice_reader.domain import Invoice
from invoice_reader.interfaces.schemas.invoice import InvoiceCreate
from invoice_reader.services.interfaces import IInvoiceRepository, IFileRepository


class InvoiceService:
    @staticmethod
    def add_invoice(
        file_repository: IFileRepository,
        invoice_repository: IInvoiceRepository,
    ) -> None:
        file_repository.store(
            file=file,
            file_data=file_data,
            invoice=invoice,
            invoice_repository=invoice_repository,
            s3_model=s3_model,
        )

    @classmethod
    def get_invoice(
        user_id: UUID, file_id: UUID, session: sqlmodel.Session
    ) -> InvoiceResponse:
        invoice_repository = InvoiceRepository(session=session)
        invoice_model = invoice_repository.get(user_id=user_id, file_id=file_id)
        if invoice_model:
            invoice = InvoiceMapper.map_invoice_model_to_invoice(
                invoice_model=invoice_model
            )
            return InvoiceMapper.map_invoice_to_response(invoice=invoice)
        raise INVOICE_NOT_FOUND

    @classmethod
    def get_invoices():
        pass

    @classmethod
    def get_paged_invoices(
        user_id: UUID, session: sqlmodel.Session, page: int, per_page: int
    ) -> PagedInvoiceResponse:
        invoice_repository = InvoiceRepository(session=session)
        invoice_models = invoice_repository.get_all(user_id=user_id)
        start = (page - 1) * per_page
        end = start + per_page
        invoices = InvoiceMapper.map_invoice_models_to_invoices(
            invoice_models=invoice_models
        )
        return PagedInvoiceResponse(
            page=page,
            per_page=per_page,
            total=len(invoice_models),
            data=InvoiceMapper.map_invoices_to_responses(invoices=invoices[start:end]),
        )

    def delete_invoice(
        file_id: uuid.UUID, user_id: uuid.UUID, session: sqlmodel.Session
    ) -> None:
        if not settings.S3_BUCKET_NAME:
            raise MISSING_ENVIRONMENT_VARIABLE_EXCEPTION
        invoice_repository = InvoiceRepository(session=session)
        invoice_model = invoice_repository.get(file_id=file_id, user_id=user_id)
        if not invoice_model:
            raise INVOICE_NOT_FOUND
        invoice = InvoiceMapper.map_invoice_model_to_invoice(
            invoice_model=invoice_model
        )
        invoice_repository.delete(file_id=file_id, user_id=user_id)

        # TODO: implement UOW and rollback
        if not invoice.s3_path:
            raise ROLLBACK
        s3 = S3.init(bucket=settings.S3_BUCKET_NAME)
        suffix = s3_utils.get_suffix_from_s3_path(s3_path=invoice.s3_path)
        s3.delete(suffix=suffix)

    def update_invoice(
        user_id: uuid.UUID,
        invoice_id: uuid.UUID,
        invoice_update: InvoiceUpdate,
        session: sqlmodel.Session,
    ) -> None:
        invoice_repository = InvoiceRepository(session=session)
        existing_invoices = invoice_repository.get_all(
            user_id=user_id,
        )
        if not existing_invoices:
            raise HTTPException(
                status_code=500,
                detail=f"Issue with updating invoice: no existing invoices found. Invoice to update: {invoice_update}",
            )
        # Check for duplicate invoice numbers (excluding the current invoice)
        if any(
            invoice.invoice_number == invoice_update.invoice_number
            and invoice.file_id != invoice_id
            for invoice in existing_invoices
        ):
            raise EXISTING_INVOICE_EXCEPTION  # There are multiple invoices with the same number: conflict
        invoice_repository.update(
            invoice_id=invoice_id,
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
