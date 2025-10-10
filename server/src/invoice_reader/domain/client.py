from functools import reduce
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from invoice_reader.domain.invoice import Amount, Currency, Invoice
from invoice_reader.utils.logger import get_logger

logger = get_logger()


class ClientData(BaseModel):
    client_name: str
    street_number: int
    street_address: str
    zipcode: str
    city: str
    country: str


class Client(BaseModel):
    id_: UUID = Field(default_factory=uuid4)
    user_id: UUID
    invoices: list[Invoice] = []
    data: ClientData

    @property
    def total_revenue(self) -> Amount:
        if not self.invoices:
            return Amount(
                currency_amounts={}, base_currency=Currency.EUR
            )  # Default to EUR with 0 amounts

        try:
            # Sum custom __add__
            total_revenue = reduce(
                lambda acc, invoice: acc + invoice.gross_amount,
                self.invoices[1:],
                self.invoices[0].gross_amount,
            )
            return total_revenue
        except Exception:
            logger.error(
                "Impossible to calculate total revenue due to mismatched currencies."
                "Invoice amounts: {}",
                [inv.gross_amount for inv in self.invoices],
            )
            return Amount(
                currency_amounts={}, base_currency=self.invoices[0].gross_amount.base_currency
            )
