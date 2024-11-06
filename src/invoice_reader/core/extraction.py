from io import BytesIO

from invoice_reader.schemas import InvoiceMetadata


def extract(file: BytesIO) -> InvoiceMetadata:
    return InvoiceMetadata()


