from datetime import datetime

import pytest
from parser.domain.parse import Annotation, ParsedData, Prediction
from parser.infrastructure.evaluator import Evaluator


annotations = [
    Annotation(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        image_uri="path",
        data=ParsedData(
            currency="USD",
            gross_amount=100.50,
            vat=20.10,
            issued_date=datetime(2023, 1, 15),
            invoice_number="INV-001",
            client_name="John Doe",
            client_street_address_number="123",
            client_street_address="Main Street",
            client_city="New York",
            client_zipcode="10001",
            client_country="USA",
        ),
    ),
    Annotation(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        image_uri="path",
        data=ParsedData(
            currency="EUR",
            gross_amount=10045,
            vat=10,
            issued_date=datetime(2025, 5, 15),
            invoice_number="k-0001",
            client_name="John Doe",
            client_street_address_number="140",
            client_street_address="Main Street",
            client_city="Paris",
            client_zipcode="75000",
            client_country="FRA",
        ),
    ),
    Annotation(
        created_at=datetime.now(),
        updated_at=datetime.now(),
        image_uri="path",
        data=ParsedData(
            currency="CZK",
            gross_amount=20000,
            vat=21,
            issued_date=datetime(2025, 2, 10),
            invoice_number="INV-002",
            client_name="Jeremy",
            client_street_address_number="02",
            client_street_address="Chardons",
            client_city="Bourges",
            client_zipcode="14000",
            client_country="FRA",
        ),
    ),
]


predictions = [
    Prediction(
        model_name="mock",
        data=ParsedData(
            currency="EUR",  # Error
            gross_amount=100,  # OK
            vat=20,  # OK
            issued_date=datetime(2023, 1, 15),
            invoice_number="INV-001",
            client_name="John  Doe",  # OK
            client_street_address_number="123",
            client_street_address="Main Street",
            client_city="Paris",  # Error
            client_zipcode="75000",  # Error
            client_country="FRA",  # Error
        ),
    ),
    Prediction(
        model_name="mock",
        data=ParsedData(
            currency="USD",  # Error
            gross_amount=4500,  # Error
            vat=10,
            issued_date=datetime(2024, 5, 15),  # Error
            invoice_number="k-0001",
            client_name="John Doe",
            client_street_address_number="140",
            client_street_address="Main Street",
            client_city="Pari s",  # OK
            client_zipcode="75 000",  # OK
            client_country="FRA",
        ),
    ),
    Prediction(
        model_name="mock",
        data=ParsedData(
            currency="CZK",
            gross_amount=20000,
            vat=21,
            issued_date=datetime(2025, 2, 10),
            invoice_number="INV-002",
            client_name="Jeremy",
            client_street_address_number="02",
            client_street_address="Chardons",
            client_city="Bourgef",  # OK
            client_zipcode="14000",
            client_country="FRA",
        ),
    ),
]


def test_evaluation():
    metrics = Evaluator.evaluate_parser(
        annotations=annotations, predictions=predictions
    )
    assert metrics.overall_precision == pytest.approx(0.79, 0.02)
    assert metrics.overall_recall == pytest.approx(0.79, 0.02)

    currentcy_metric = [
        metric_field
        for metric_field in metrics.field_metrics
        if metric_field.name == "currency"
    ][0]

    issued_date_metric = [
        metric_field
        for metric_field in metrics.field_metrics
        if metric_field.name == "issued_date"
    ][0]

    city_metric = [
        metric_field
        for metric_field in metrics.field_metrics
        if metric_field.name == "client_city"
    ][0]

    assert currentcy_metric.precision == pytest.approx(0.33, 0.03)
    assert issued_date_metric.precision == pytest.approx(0.66, 0.03)
    assert city_metric.precision == pytest.approx(0.66, 0.03)


def test_compare_strings():
    assert Evaluator._calculate_str("john doe", "John  Doe")
    assert Evaluator._calculate_str("Paris", "Paric")
    assert Evaluator._calculate_str("Bourges", "Bourgef")
    assert not Evaluator._calculate_str("New York", "Naw Fork")
