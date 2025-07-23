import uuid
from datetime import date

from pydantic import BaseModel, Field


class Insight(BaseModel):
    """User feedback on model prediction."""

    insight_id: uuid.UUID = Field(default_factory=uuid.uuid4())
    prediction_id: uuid.UUID
    insight: dict
    request_id: str
    created_at: date = Field(default_factory=date.today)
