from abc import ABC, abstractmethod
from uuid import UUID
from typing import Sequence

from invoice_reader.domain import Invoice


class IInvoiceRepository(ABC):
    @abstractmethod
    def add(
        self,
        user_id: UUID,
    ) -> None:
        pass

    @abstractmethod
    def update(self, invoice_id: UUID, invoice: Invoice) -> None:
        pass

    @abstractmethod
    def get(self, invoice_id: UUID, user_id: UUID) -> Invoice | None:
        pass

    @abstractmethod
    def delete(self, invoice_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    def get_all(self, user_id: UUID) -> Sequence[Invoice]:
        pass

    @abstractmethod
    def get_by_invoice_number(
        self,
        invoice_number: str,
        user_id: UUID,
    ) -> Invoice | None:
        pass
