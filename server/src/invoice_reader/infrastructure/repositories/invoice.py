from uuid import UUID

from sqlmodel import Session, select

from invoice_reader.domain.invoice import Invoice
from invoice_reader.infrastructure.models import InvoiceModel
from invoice_reader.services.interfaces.repositories import IInvoiceRepository


class InMemoryInvoiceRepository(IInvoiceRepository):
    def __init__(self):
        self.invoices: dict[UUID, Invoice] = {}

    def add(self, invoice: Invoice) -> None:
        self.invoices[invoice.id_] = invoice

    def get(self, invoice_id: UUID) -> Invoice | None:
        return self.invoices.get(invoice_id)

    def update(self, invoice: Invoice) -> None:
        if invoice.id_ in self.invoices:
            self.invoices[invoice.id_] = invoice

    def delete(self, invoice_id: UUID) -> None:
        if invoice_id in self.invoices:
            self.invoices.pop(invoice_id)

    def get_all(self, user_id: UUID) -> list[Invoice]:
        return [invoice for invoice in self.invoices.values() if invoice.user_id == user_id]

    def get_by_invoice_number(self, invoice_number: str, user_id: UUID) -> Invoice | None:
        for invoice in self.invoices.values():
            if invoice.user_id == user_id and invoice.invoice_number == invoice_number:
                return invoice


class SQLModelInvoiceRepository(IInvoiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_model(self, invoice: Invoice) -> InvoiceModel:
        """Convert domain entity to infrastructure model."""
        return InvoiceModel(
            invoice_id=invoice.id_,
            user_id=invoice.user_id,
            client_id=invoice.client_id,
            currency=invoice.currency,
            invoice_number=invoice.invoice_number,
            gross_amount=invoice.gross_amount,
            vat=invoice.vat,
            description=invoice.description,
            invoiced_date=invoice.issued_date,
            paid_date=invoice.paid_date,
            storage_path=invoice.storage_path,
        )

    def _to_entity(self, model: InvoiceModel) -> Invoice:
        """Convert infrastructure model to domain entity."""
        return Invoice(
            id_=model.invoice_id,
            user_id=model.user_id,
            client_id=model.client_id,
            storage_path=model.storage_path,
            invoice_number=model.invoice_number,
            gross_amount=model.gross_amount,
            vat=model.vat,
            description=model.description,
            issued_date=model.invoiced_date,
            paid_date=model.paid_date,
            currency=model.currency,
        )

    def add(self, invoice: Invoice) -> None:
        invoice_model = self._to_model(invoice)
        self.session.add(invoice_model)
        self.session.commit()

    def get(self, invoice_id: UUID) -> Invoice | None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.invoice_id == invoice_id)
        ).one_or_none()
        return self._to_entity(invoice_model) if invoice_model else None

    def delete(self, invoice_id: UUID) -> None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.invoice_id == invoice_id)
        ).one()
        self.session.delete(invoice_model)
        self.session.commit()

    def get_all(self, user_id: UUID) -> list[Invoice]:
        invoice_models = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.user_id == user_id)
        ).all()
        return [self._to_entity(model) for model in invoice_models]

    def get_by_invoice_number(self, invoice_number: str, user_id: UUID) -> Invoice | None:
        invoice_model = self.session.exec(
            select(InvoiceModel).where(
                InvoiceModel.invoice_number == invoice_number,
                InvoiceModel.user_id == user_id,
            )
        ).one_or_none()
        return self._to_entity(invoice_model) if invoice_model else None

    def update(self, invoice: Invoice) -> None:
        existing_invoice_model = self.session.exec(
            select(InvoiceModel).where(InvoiceModel.invoice_id == invoice.id_)
        ).one()

        # Update existing model with new values
        updated_data = self._to_model(invoice).model_dump(exclude={"id"})
        for key, value in updated_data.items():
            setattr(existing_invoice_model, key, value)

        self.session.add(existing_invoice_model)
        self.session.commit()
