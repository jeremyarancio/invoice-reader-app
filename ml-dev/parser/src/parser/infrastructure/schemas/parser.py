from typing import Annotated
from datetime import date

from pydantic import BaseModel, Field

from parser.domain.parse import ParsedData, Prediction


class ParsedInvoice(BaseModel):
    currency: Annotated[
        str,
        Field(
            description="The currency of the invoice in respect of ISO 4217 standard: usd-eur-czk."
        ),
    ]
    gross_amount: Annotated[float, Field(description="The gross amount before tax.")]
    vat: Annotated[
        float,
        Field(
            description="The value-added tax amount in percentage (20 for 20%, 4.5 for 4.5%...)"
        ),
    ]
    issued_date: Annotated[date, Field(description="The date the invoice was issued.")]
    invoice_number: Annotated[
        str, Field(description="The unique identifier for the invoice.")
    ]
    client_name: Annotated[str, Field(description="The name of the client.")]
    client_street_address_number: Annotated[
        str, Field(description="The street address number of the client.")
    ]
    client_street_address: str
    client_city: str
    client_zipcode: str
    client_country: str

    def to_prediction(self, model_name: str) -> Prediction:
        return Prediction(
            model_name=model_name,
            data=ParsedData(
                currency=self.currency,
                gross_amount=self.gross_amount,
                vat=self.vat,
                issued_date=self.issued_date,
                invoice_number=self.invoice_number,
                client_name=self.client_name,
                client_street_address_number=self.client_street_address_number,
                client_street_address=self.client_street_address,
                client_city=self.client_city,
                client_zipcode=self.client_zipcode,
                client_country=self.client_country,
            ),
        )
