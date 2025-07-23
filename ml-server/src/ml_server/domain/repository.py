"""Repository interface for Prediction aggregate."""

import uuid
from abc import ABC, abstractmethod
from typing import List

from ml_server.domain.prediction import Prediction


class PredictionRepository(ABC):
    """Abstract repository interface for Prediction aggregate."""

    @abstractmethod
    def create(self, prediction: Prediction) -> Prediction:
        """Save a prediction to the repository."""
        pass

    @abstractmethod
    def find_by_id(self, prediction_id: uuid.UUID) -> Prediction | None:
        """Find a prediction by its ID."""
        pass

    @abstractmethod
    def find_by_request_id(self, request_id: str) -> List[Prediction]:
        """Find predictions by request ID."""
        pass

    @abstractmethod
    def find_by_model_id(self, model_id: str) -> List[Prediction]:
        """Find predictions by model ID."""
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Prediction]:
        """Find all predictions with pagination."""
        pass

    @abstractmethod
    def update(self, prediction: Prediction) -> Prediction:
        """Update an existing prediction."""
        pass

    @abstractmethod
    def delete(self, prediction_id: uuid.UUID) -> bool:
        """Delete a prediction by its ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def exists(self, prediction_id: uuid.UUID) -> bool:
        """Check if a prediction exists by its ID."""
        pass
