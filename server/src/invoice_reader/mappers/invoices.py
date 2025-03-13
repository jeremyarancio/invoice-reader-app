import uuid
from typing import Sequence

from invoice_reader.models import InvoiceModel
from invoice_reader.schemas.invoices import (
    Invoice,
    InvoiceBase,
    InvoiceCreate,
    InvoiceResponse,
)


class InvoiceMapper:
    @staticmethod
    def map_invoice_model_to_invoice(
        invoice_model: InvoiceModel,
    ) -> Invoice:
        return Invoice.model_validate(invoice_model.model_dump())

    @classmethod
    def map_invoice_models_to_invoices(
        cls,
        invoice_models: Sequence[InvoiceModel],
    ) -> list[Invoice]:
        return [
            cls.map_invoice_model_to_invoice(invoice_model=invoice_model)
            for invoice_model in invoice_models
        ]

    @staticmethod
    def map_invoice_to_response(
        invoice: Invoice,
    ) -> InvoiceResponse:
        return InvoiceResponse(
            invoice_id=invoice.file_id,
            client_id=invoice.client_id,
            s3_path=invoice.s3_path,
            currency_id=invoice.currency_id,
            data=InvoiceBase.model_validate(invoice.model_dump()),
        )

    @classmethod
    def map_invoices_to_responses(
        cls,
        invoices: list[Invoice],
    ) -> list[InvoiceResponse]:
        return [cls.map_invoice_to_response(invoice) for invoice in invoices]

    @staticmethod
    def map_invoice_create_to_invoice(
        invoice_create: InvoiceCreate,
    ) -> Invoice:
        return Invoice(
            client_id=invoice_create.client_id,
            currency_id=invoice_create.currency_id,
            **invoice_create.invoice.model_dump(),
        )

    @staticmethod
    def map_invoice_to_model(
        invoice: Invoice,
        user_id: uuid.UUID,
    ) -> InvoiceModel:
        return InvoiceModel(user_id=user_id, **invoice.model_dump())
