from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.user import InMemoryUserRepository

pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.domain.client",
    "tests.fixtures.domain.invoice",
    "tests.fixtures.domain.user",
]

InMemoryInvoiceRepository.init()
InMemoryClientRepository.init()
