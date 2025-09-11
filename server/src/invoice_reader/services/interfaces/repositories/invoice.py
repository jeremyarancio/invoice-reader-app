from abc import ABC, abstractmethod

from invoice_reader.domain.invoice import Invoice, InvoiceID
from invoice_reader.domain.user import UserID


class IInvoiceRepository(ABC):
    @abstractmethod
    def add(self, invoice: Invoice) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, invoice: Invoice) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, invoice_id: InvoiceID) -> Invoice | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, invoice_id: InvoiceID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: UserID) -> list[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def get_by_invoice_number(self, invoice_number: str, user_id: UserID) -> Invoice | None:
        raise NotImplementedError
