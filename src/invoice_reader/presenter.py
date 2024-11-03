from io import BytesIO

from invoice_reader.core import extract, store
from invoice_reader.core.schemas import InvoiceMetadata


def upload(file: BytesIO) -> InvoiceMetadata:
    invoice_metadata = extract.extract(file=file)
    if invoice_metadata.is_complete():
        store.store()
    return invoice_metadata  