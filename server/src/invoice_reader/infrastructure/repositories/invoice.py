from uuid import UUID, uuid4

from sqlmodel import Session, select

from invoice_reader.services.interfaces.repositories import IInvoiceRepository
from invoice_reader.domain import Invoice, InvoiceID
from invoice_reader.infrastructure.models import InvoiceModel


class SQLModelInvoiceRepository(IInvoiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, invoice: Invoice) -> None:
        invoice_model = InvoiceModel(
            file_id=invoice.id_,
            user_id=invoice.user_id,
            client_id=invoice.client_id,
            currency_id=uuid4(),  # TODO: Migrate for currency string directly
            invoice_number=invoice.data.invoice_number,
            amount_excluding_tax=invoice.data.gross_amount,
            vat=invoice.data.vat,
            description=invoice.data.description,
            invoiced_date=invoice.data.issued_date,
            paid_date=invoice.data.paid_date,
            s3_path=invoice.file.storage_path,
        )
        self.session.add(invoice_model)
        self.session.commit()

    def update(self, invoice):
        pass

    def get(self, invoice_id: InvoiceID) -> Invoice | None:
        self.session.exec(
            select(InvoiceModel).where(InvoiceModel.file_id == invoice_id)
        ).one_or_none()

    def delete(self, invoice_id: InvoiceID) -> None:
        pass

    def get_all(self, user_id: UUID) -> list[Invoice]:
        invoice_models = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        return [
            Invoice(
                id_=invoice_model.file_id,
                user_id=invoice_model.user_id,
                client_id=invoice_model.client_id,
                file=invoice_model.s3_path,
                data=Invoice,
            )
            for invoice_model in invoice_models
        ]

    def get_by_invoice_number(self, invoice_number, user_id):
        return super().get_by_invoice_number(invoice_number, user_id)
