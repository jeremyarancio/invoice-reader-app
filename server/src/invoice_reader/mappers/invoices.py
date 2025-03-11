import uuid
from typing import Sequence

from invoice_reader.models import InvoiceModel
from invoice_reader.schemas import invoice_schema


class InvoiceMapper:
    @staticmethod
    def map_invoice_model_to_invoice(
        invoice_model: InvoiceModel,
    ) -> invoice_schema.InvoicePresenter:
        return invoice_schema.InvoicePresenter.model_validate(
            invoice_model.model_dump()
        )

    @classmethod
    def map_invoice_models_to_invoices(
        cls,
        invoice_models: Sequence[InvoiceModel],
    ) -> list[invoice_schema.InvoicePresenter]:
        return [
            cls.map_invoice_model_to_invoice(invoice_model=invoice_model)
            for invoice_model in invoice_models
        ]

    @staticmethod
    def map_invoice_to_response(
        invoice: invoice_schema.InvoicePresenter,
        client_id: uuid.UUID,
    ) -> invoice_schema.InvoiceResponse:
        return invoice_schema.InvoiceResponse(
            client_id=client_id,
            invoice_id=invoice.file_id,
            s3_path=invoice.s3_path,
            data=invoice.model_dump(),
        )

    @classmethod
    def map_invoices_to_responses(
        cls,
        invoices: list[invoice_schema.InvoicePresenter],
    ) -> list[invoice_schema.InvoiceResponse]:
        return [cls.map_invoice_to_response(invoice) for invoice in invoices]

    @staticmethod
    def map_invoice_create_to_invoice(
        invoice_create: invoice_schema.InvoiceCreate,
    ) -> invoice_schema.InvoicePresenter:
        return invoice_schema.InvoicePresenter(
            client_id=invoice_create.client_id, **invoice_create.invoice.model_dump()
        )

    @staticmethod
    def map_invoice_to_model(
        invoice: invoice_schema.InvoicePresenter,
        user_id: uuid.UUID,
    ) -> InvoiceModel:
        return InvoiceModel(user_id=user_id, **invoice.model_dump())

    @staticmethod
    def map_invoice_update_to_invoice(
        invoice_update: invoice_schema.InvoiceUpdate,
    ) -> invoice_schema.InvoicePresenter:
        return invoice_schema.InvoicePresenter.model_validate(
            invoice_update.model_dump()
        )
