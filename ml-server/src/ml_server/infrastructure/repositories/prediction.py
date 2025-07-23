"""In-memory implementation of PredictionRepository for testing purposes."""

import uuid
from typing import Dict, List, Optional

from ml_server.domain.prediction.prediction import Prediction
from ml_server.domain.prediction.prediction_repository import PredictionRepository


class InMemoryPredictionRepository(PredictionRepository):
    """In-memory implementation of PredictionRepository for testing."""

    def __init__(self):
        self._predictions: Dict[uuid.UUID, Prediction] = {}

    async def save(self, prediction: Prediction) -> Prediction:
        """Save a prediction to the in-memory store."""
        self._predictions[prediction.prediction_id] = prediction
        return prediction

    async def find_by_id(self, prediction_id: uuid.UUID) -> Optional[Prediction]:
        """Find a prediction by its ID."""
        return self._predictions.get(prediction_id)

    async def find_by_request_id(self, request_id: str) -> List[Prediction]:
        """Find predictions by request ID."""
        return [
            prediction
            for prediction in self._predictions.values()
            if prediction.request_id == request_id
        ]

    async def find_by_model_id(self, model_id: str) -> List[Prediction]:
        """Find predictions by model ID."""
        return [
            prediction
            for prediction in self._predictions.values()
            if prediction.model_id == model_id
        ]

    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Prediction]:
        """Find all predictions with pagination."""
        all_predictions = list(self._predictions.values())
        return all_predictions[offset : offset + limit]

    async def update(self, prediction: Prediction) -> Prediction:
        """Update an existing prediction."""
        if prediction.prediction_id not in self._predictions:
            raise ValueError(f"Prediction {prediction.prediction_id} not found")

        self._predictions[prediction.prediction_id] = prediction
        return prediction

    async def delete(self, prediction_id: uuid.UUID) -> bool:
        """Delete a prediction by its ID."""
        if prediction_id in self._predictions:
            del self._predictions[prediction_id]
            return True
        return False

    async def exists(self, prediction_id: uuid.UUID) -> bool:
        """Check if a prediction exists by its ID."""
        return prediction_id in self._predictions

    def clear(self) -> None:
        """Clear all predictions (for testing purposes)."""
        self._predictions.clear()

    def count(self) -> int:
        """Get the total number of predictions (for testing purposes)."""
        return len(self._predictions)
