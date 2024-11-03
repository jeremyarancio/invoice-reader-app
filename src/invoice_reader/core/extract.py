from io import BytesIO

from invoice_reader.core.schemas import InvoiceMetadata


def extract(file: BytesIO) -> InvoiceMetadata:
    return InvoiceMetadata()