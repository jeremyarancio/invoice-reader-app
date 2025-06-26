from uuid import UUID

from pydantic import ValidationError

from invoice_reader.infrastructure.togetherai import InvoiceParsingSchema
from invoice_reader.repository import ClientRepository, CurrencyRepository
from invoice_reader.schemas.parser import (
    Address,
    ClientDataExtraction,
    InvoiceDataExtraction,
    InvoiceExtraction,
    SellerDataExtraction,
)
from invoice_reader.utils.logger import get_logger

LOGGER = get_logger(__name__)


def find_currency_id(
    currency: str, currency_repository: CurrencyRepository
) -> UUID | None:
    currencies = currency_repository.get_all()
    for curr in currencies:
        if curr.currency == currency:
            return curr.id


def find_client_id(
    client_name: str, client_repository: ClientRepository, user_id: UUID
) -> UUID | None:
    """Finds the client ID by client name."""
    client = client_repository.get_by_name(user_id=user_id, client_name=client_name)
    if client:
        return client.client_id
    return None


def map_invoice_parsing_to_response(
    extraction: InvoiceParsingSchema,
    currency_repository: CurrencyRepository,
    client_repository: ClientRepository,
    user_id: UUID,
) -> InvoiceExtraction:
    """Maps the extracted data to the InvoiceData model."""
    try:
        invoice_extract = InvoiceDataExtraction(
            gross_amount=extraction.gross_amount,
            vat=extraction.vat,
            issued_date=extraction.issued_date,
            invoice_number=extraction.invoice_number,
            invoice_description=extraction.invoice_description,
            currency_id=find_currency_id(extraction.currency, currency_repository),
        )
        client_extract = ClientDataExtraction(
            client_id=find_client_id(
                extraction.buyer_name,
                client_repository=client_repository,
                user_id=user_id,
            ),
            address=Address(
                street_address=extraction.buyer_address,
                zipcode=extraction.buyer_address_zipcode,
                city=extraction.buyer_address_city,
                country=extraction.buyer_address_country,
            ),
        )
        seller_extract = SellerDataExtraction(
            name=extraction.seller_name,
            address=Address(
                street_address=extraction.seller_address,
                zipcode=extraction.seller_address_zipcode,
                city=extraction.seller_address_city,
                country=extraction.seller_address_country,
            ),
        )
        return InvoiceExtraction(
            invoice=invoice_extract, client=client_extract, seller=seller_extract
        )
    except ValidationError as e:
        LOGGER.error(f"Validation error while mapping invoice parsing: {e}")
        raise ValueError("Invalid data format received from invoice parsing") from e
