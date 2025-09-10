from invoice_reader.services.interfaces.repositories import (
    IClientRepository,
    IFileRepository,
    IInvoiceRepository,
    IUserRepository,
)


# TODO: implement dependency injection
def get_file_repository() -> IFileRepository:
    raise NotImplementedError


def get_invoice_repository() -> IInvoiceRepository:
    raise NotImplementedError


def get_client_repository() -> IClientRepository:
    raise NotImplementedError


def get_user_repository() -> IUserRepository:
    raise NotImplementedError
