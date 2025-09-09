from invoice_reader.services.interfaces.repositories import IFileRepository, IInvoiceRepository


def get_file_repository() -> IFileRepository:
    raise NotImplementedError


def get_invoice_repository() -> IInvoiceRepository:
    raise NotImplementedError