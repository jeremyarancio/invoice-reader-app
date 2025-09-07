from sqlmodel import Session, select

from invoice_reader.services.interfaces import IInvoiceRepository
from invoice_reader.domain import Invoice, InvoiceID
from invoice_reader.infrastructure.models import InvoiceModel


class SQLModelInvoiceRepository(IInvoiceRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, invoice: Invoice) -> None:
        invoice_model = InvoiceModel()
        self.session.add(invoice_model)
        self.session.commit()
