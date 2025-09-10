from uuid import UUID

from sqlmodel import Session, select

from invoice_reader.domain import Invoice, InvoiceData, InvoiceID
from invoice_reader.infrastructure.models import InvoiceModel
from invoice_reader.services.interfaces.repositories import IInvoiceRepository


class SQLModelInvoiceRepository(IInvoiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, invoice: Invoice) -> None:
        invoice_model = InvoiceModel(
            invoice_id=invoice.id_,
            user_id=invoice.user_id,
            client_id=invoice.client_id,
            currency=invoice.data.currency,
            invoice_number=invoice.data.invoice_number,
            amount_excluding_tax=invoice.data.gross_amount,
            vat=invoice.data.vat,
            description=invoice.data.description,
            invoiced_date=invoice.data.issued_date,
            paid_date=invoice.data.paid_date,
            storage_path=invoice.storage_path,
        )
        self.session.add(invoice_model)
        self.session.commit()

    def get(self, invoice_id: InvoiceID) -> Invoice | None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.invoice_id == invoice_id)
        ).one_or_none()
        if invoice_model:
            return Invoice(
                id_=invoice_model.invoice_id,
                user_id=invoice_model.user_id,
                client_id=invoice_model.client_id,
                storage_path=invoice_model.storage_path,
                data=InvoiceData(
                    invoice_number=invoice_model.invoice_number,
                    gross_amount=invoice_model.amount_excluding_tax,
                    vat=invoice_model.vat,
                    description=invoice_model.description,
                    issued_date=invoice_model.invoiced_date,
                    paid_date=invoice_model.paid_date,
                    currency=invoice_model.currency,
                ),
            )

    def delete(self, invoice_id: InvoiceID) -> None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.invoice_id == invoice_id)
        ).one()
        self.session.delete(invoice_model)
        self.session.commit()

    def get_all(self, user_id: UUID) -> list[Invoice]:
        invoice_models = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        return [
            Invoice(
                id_=invoice_model.invoice_id,
                user_id=invoice_model.user_id,
                client_id=invoice_model.client_id,
                storage_path=invoice_model.storage_path,
                data=InvoiceData(
                    invoice_number=invoice_model.invoice_number,
                    gross_amount=invoice_model.amount_excluding_tax,
                    vat=invoice_model.vat,
                    description=invoice_model.description,
                    issued_date=invoice_model.invoiced_date,
                    paid_date=invoice_model.paid_date,
                    currency=invoice_model.currency,
                ),
            )
            for invoice_model in invoice_models
        ]

    def get_by_invoice_number(self, invoice_number: str, user_id: UUID) -> Invoice | None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number,
                InvoiceModel.user_id == user_id,
            )
        ).one_or_none()
        if invoice_model:
            return Invoice(
                id_=invoice_model.invoice_id,
                user_id=invoice_model.user_id,
                client_id=invoice_model.client_id,
                storage_path=invoice_model.storage_path,
                data=InvoiceData(
                    invoice_number=invoice_model.invoice_number,
                    gross_amount=invoice_model.amount_excluding_tax,
                    vat=invoice_model.vat,
                    description=invoice_model.description,
                    issued_date=invoice_model.invoiced_date,
                    paid_date=invoice_model.paid_date,
                    currency=invoice_model.currency,
                ),
            )

    def update(self, invoice: Invoice) -> None:
        invoice_model = InvoiceModel(
            invoice_id=invoice.id_,
            user_id=invoice.user_id,
            client_id=invoice.client_id,
            storage_path=invoice.storage_path,
            currency=invoice.data.currency,
            invoice_number=invoice.data.invoice_number,
            amount_excluding_tax=invoice.data.gross_amount,
            vat=invoice.data.vat,
            description=invoice.data.description,
            invoiced_date=invoice.data.issued_date,
            paid_date=invoice.data.paid_date,
        )
        self.session.add(invoice_model)
        self.session.commit()
