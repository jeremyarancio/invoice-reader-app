from invoice_reader.services.interfaces import IFileRepository, IInvoiceRepository


def get_file_repository() -> IFileRepository:
    raise NotImplementedError


def get_invoice_repository() -> IInvoiceRepository:
    raise NotImplementedError