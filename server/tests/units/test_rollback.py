import pytest

from invoice_reader.domain.invoice import File, Invoice
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.services.exceptions import RollbackException
from invoice_reader.services.invoice import InvoiceService


@pytest.fixture
def invoice_repository():
    return InMemoryInvoiceRepository()


@pytest.fixture
def file_repository():
    return InMemoryFileRepository()


def test_rollback_add(
    invoice_repository: InMemoryInvoiceRepository,
    file_repository: InMemoryFileRepository,
    existing_invoice: Invoice,
    existing_file: File,
):
    with pytest.raises(RollbackException):
        InvoiceService._rollback_add(  # type: ignore (protected)
            invoice_repository=invoice_repository,
            file_repository=file_repository,
            invoice=existing_invoice,
            error=Exception("This is an error."),
        )
    assert InMemoryInvoiceRepository().get(invoice_id=existing_invoice.id_) is None
    assert InMemoryFileRepository().get(storage_path=existing_file.storage_path) is None
