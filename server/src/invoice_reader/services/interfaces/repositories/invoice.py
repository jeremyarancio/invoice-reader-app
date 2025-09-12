from abc import ABC, abstractmethod

from invoice_reader.domain.invoice import UUID, Invoice


class IInvoiceRepository(ABC):
    @abstractmethod
    def add(self, invoice: Invoice) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, invoice: Invoice) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, invoice_id: UUID) -> Invoice | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, invoice_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: UUID) -> list[Invoice]:
        raise NotImplementedError

    @abstractmethod
    def get_by_invoice_number(self, invoice_number: str, user_id: UUID) -> Invoice | None:
        raise NotImplementedError
