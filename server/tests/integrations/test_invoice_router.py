from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from invoice_reader.domain.client import Client
from invoice_reader.domain.invoice import Invoice, InvoiceUpdate
from invoice_reader.domain.user import User
from invoice_reader.infrastructure.parser import TestParser
from invoice_reader.infrastructure.repositories.client import InMemoryClientRepository
from invoice_reader.infrastructure.repositories.file import InMemoryFileRepository
from invoice_reader.infrastructure.repositories.invoice import InMemoryInvoiceRepository
from invoice_reader.interfaces.api.main import app
from invoice_reader.interfaces.dependencies.auth import get_current_user_id
from invoice_reader.interfaces.dependencies.parser import get_parser
from invoice_reader.interfaces.dependencies.repository import (
    get_client_repository,
    get_file_repository,
    get_invoice_repository,
)
from invoice_reader.interfaces.schemas.invoice import (
    InvoiceCreate,
    InvoiceResponse,
    PagedInvoiceResponse,
)
from invoice_reader.interfaces.schemas.parser import ParserResponse


def _test_get_invoice_repository():
    return InMemoryInvoiceRepository()


def create_test_get_current_user_id(user: User):
    def _test_get_current_user_id():
        return user.id_

    return _test_get_current_user_id


def _test_get_parser():
    return TestParser()


def _test_get_file_repository():
    return InMemoryFileRepository()


def _test_get_client_repository():
    return InMemoryClientRepository()


@pytest.fixture
def test_client(user: User):
    client = TestClient(app)
    app.dependency_overrides[get_invoice_repository] = _test_get_invoice_repository
    app.dependency_overrides[get_parser] = _test_get_parser
    app.dependency_overrides[get_current_user_id] = create_test_get_current_user_id(user=user)
    app.dependency_overrides[get_file_repository] = _test_get_file_repository
    app.dependency_overrides[get_client_repository] = _test_get_client_repository
    yield client
    app.dependency_overrides.clear()


def test_add_invoice(
    test_client: TestClient, upload_files: Any, invoice_create: InvoiceCreate, user: User
):
    response = test_client.post(
        "/v1/invoices/",
        files=upload_files,
        data={"data": invoice_create.model_dump_json()},
    )
    assert response.status_code == 201
    invoice = InMemoryInvoiceRepository().get_by_invoice_number(
        invoice_create.invoice.invoice_number, user_id=user.id_
    )
    assert invoice
    assert invoice.invoice_number == invoice_create.invoice.invoice_number


def test_add_exisiting_invoice(
    test_client: TestClient,
    upload_files: Any,
    invoice_create: InvoiceCreate,
    existing_invoice: Invoice,
):
    response = test_client.post(
        "/v1/invoices/", files=upload_files, data={"data": invoice_create.model_dump_json()}
    )
    assert response.status_code == 409


def test_get_invoice(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.get(f"/v1/invoices/{existing_invoice.id_}")
    invoice_response = InvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert invoice_response.invoice_id == existing_invoice.id_
    assert invoice_response.data.invoice_number == existing_invoice.invoice_number


# TODO: Get invoices
# TODO: Update with existing invoice number (require several invoices already stored)


def test_update_invoice(
    test_client: TestClient, invoice_update: InvoiceUpdate, existing_invoice: Invoice
):
    response = test_client.put(
        f"/v1/invoices/{existing_invoice.id_}",
        data=invoice_update.model_dump_json(),  # type: ignore
    )
    assert response.status_code == 204
    updated_invoice = InMemoryInvoiceRepository().get(invoice_id=existing_invoice.id_)
    assert updated_invoice is not None
    assert updated_invoice.gross_amount == invoice_update.gross_amount
    assert updated_invoice.vat == invoice_update.vat
    assert updated_invoice.description == invoice_update.description


def test_delete_invoice(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.delete(f"/v1/invoices/{existing_invoice.id_}")
    assert response.status_code == 204
    deleted_invoice = InMemoryInvoiceRepository().get(invoice_id=existing_invoice.id_)
    assert deleted_invoice is None


def test_get_paged_invoices(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.get("/v1/invoices")
    paged_invoices = PagedInvoiceResponse.model_validate(response.json())
    assert response.status_code == 200
    assert paged_invoices.total == 1
    assert paged_invoices.data[0].invoice_id == existing_invoice.id_


def test_file_storage_url(test_client: TestClient, existing_invoice: Invoice):
    response = test_client.get(f"/v1/invoices/{existing_invoice.id_}/url")
    assert response.status_code == 200
    assert response.json() == "fake_url"


def test_get_invoice_not_found(test_client: TestClient):
    response = test_client.get(f"/v1/invoices/{uuid4()}")
    assert response.status_code == 404


def test_delete_invoice_not_found(test_client: TestClient):
    response = test_client.delete(f"/v1/invoices/{uuid4()}")
    assert response.status_code == 404


def test_parser_with_client_not_found(test_client: TestClient, upload_files: Any):
    response = test_client.post("/v1/invoices/parse", files=upload_files)
    assert response.status_code == 200
    parsed_data = ParserResponse.model_validate(response.json())
    assert parsed_data.client is None


def test_parser_with_client_found(
    test_client: TestClient, upload_files: Any, existing_client: Client
):
    response = test_client.post("/v1/invoices/parse", files=upload_files)
    assert response.status_code == 200
    parser_response = ParserResponse.model_validate(response.json())
    assert parser_response.client is not None
    assert parser_response.client.id_ == existing_client.id_
