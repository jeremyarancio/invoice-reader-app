from pydantic import BaseModel


class FieldMetrics(BaseModel):
    """Metrics for a single field."""

    precision: float
    recall: float
    f1_score: float


class Metrics(BaseModel):
    """Overall and per-field evaluation metrics."""

    # Overall metrics (macro-averaged across all fields)
    overall_precision: float
    overall_recall: float
    overall_f1_score: float

    # Per-field metrics
    currency: FieldMetrics
    gross_amount: FieldMetrics
    vat: FieldMetrics
    issued_date: FieldMetrics
    invoice_number: FieldMetrics
    client_name: FieldMetrics
    client_street_address_number: FieldMetrics
    client_street_address: FieldMetrics
    client_city: FieldMetrics
    client_zipcode: FieldMetrics
    client_country: FieldMetrics
