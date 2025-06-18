import uuid
from typing import Sequence

from invoice_reader.models import InvoiceModel
from invoice_reader.schemas.invoices import (
    Invoice,
    InvoiceBase,
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
)


class InvoiceMapper:
    @staticmethod
    def map_invoice_model_to_invoice(
        invoice_model: InvoiceModel,
    ) -> Invoice:
        return Invoice(
            file_id=invoice_model.file_id,
            s3_path=invoice_model.s3_path,
            client_id=invoice_model.client_id,
            currency_id=invoice_model.currency_id,
            invoice_number=invoice_model.invoice_number,
            gross_amount=invoice_model.amount_excluding_tax,
            invoiced_date=invoice_model.invoiced_date,
            description=invoice_model.description,
            vat=invoice_model.vat,
            paid_date=invoice_model.paid_date,
        )

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
            data=InvoiceBase(
                invoice_number=invoice.invoice_number,
                gross_amount=invoice.gross_amount,
                vat=invoice.vat,
                invoiced_date=invoice.invoiced_date,
                paid_date=invoice.paid_date,
                description=invoice.description,
            ),
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
            gross_amount=invoice_create.invoice.gross_amount,
            vat=invoice_create.invoice.vat,
            invoiced_date=invoice_create.invoice.invoiced_date,
            paid_date=invoice_create.invoice.paid_date,
            invoice_number=invoice_create.invoice.invoice_number,
            description=invoice_create.invoice.description,
        )

    @staticmethod
    def map_invoice_to_model(
        invoice: Invoice,
        user_id: uuid.UUID,
    ) -> InvoiceModel:
        return InvoiceModel(
            user_id=user_id,
            file_id=invoice.file_id,
            s3_path=invoice.s3_path,
            client_id=invoice.client_id,
            currency_id=invoice.currency_id,
            amount_excluding_tax=invoice.gross_amount,
            invoice_number=invoice.invoice_number,
            invoiced_date=invoice.invoiced_date,
            description=invoice.description,
            vat=invoice.vat,
            paid_date=invoice.paid_date,
        )

    @staticmethod
    def map_invoice_update_for_model(invoice_update: InvoiceUpdate) -> dict:
        return {
            "invoice_number": invoice_update.invoice_number,
            "vat": invoice_update.vat,
            "invoiced_date": invoice_update.invoiced_date,
            "paid_date": invoice_update.paid_date,
            "description": invoice_update.description,
            "currency_id": invoice_update.currency_id,
            "client_id": invoice_update.client_id,
            "amount_excluding_tax": invoice_update.gross_amount,
        }
