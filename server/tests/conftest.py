from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.infrastructure.repositories.user import InMemoryUserRepository

pytest_plugins = [
    "tests.fixtures.db",
    "tests.fixtures.entities.client",
    "tests.fixtures.entities.invoice",
    "tests.fixtures.entities.user",
]

# Create persistent in memory database
InMemoryInvoiceRepository.init()
InMemoryClientRepository.init()
InMemoryUserRepository.init()
