from pydantic import BaseModel


class FieldMetrics(BaseModel):
    """Metrics for a single field."""

    name: str
    precision: float
    recall: float
    f1_score: float


class Metrics(BaseModel):
    """Overall and per-field evaluation metrics."""

    overall_precision: float
    overall_recall: float
    overall_f1_score: float
    field_metrics: list[FieldMetrics]
