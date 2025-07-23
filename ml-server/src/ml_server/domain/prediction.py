import uuid
from datetime import date
from typing import Any, Dict

from pydantic import BaseModel, Field


class Prediction(BaseModel):
    """Model prediction aggregate"""

    prediction_id: uuid.UUID = Field(default_factory=uuid.uuid4())
    model_id: str
    prediction: dict
    request_id: str
    created_at: date = Field(default_factory=date.today)

    def update_prediction(self, new_prediction: Dict[str, Any]) -> None:
        """Update the prediction data."""
        self.prediction = new_prediction

    def is_valid(self) -> bool:
        """Validation logic to implement."""
        return True

    def __str__(self) -> str:
        return f"Prediction(id={self.prediction_id}, model_id={self.model_id}, request_id={self.request_id})"

    def __repr__(self) -> str:
        return self.__str__()
