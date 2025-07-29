"""Domain service for Predictions."""

import uuid
from typing import Any, Dict, List, Optional

from ml_server.domain.prediction import Prediction
from ml_server.domain.repository import PredictionRepository
from ml_server.application.exceptions import InvalidPredictionError


class PredictionService:
    """Domain service for Prediction aggregate operations."""

    def __init__(self, repository: PredictionRepository):
        self._repository = repository

    def save_prediction(
        self,
        model_id: str,
        prediction_data: dict,
        request_id: str,
    ) -> Prediction:
        prediction = Prediction(
            model_id=model_id,
            prediction=prediction_data,
            request_id=request_id,
        )
        if not prediction.is_valid():
            raise InvalidPredictionError("Prediction data validation failed")
        return self._repository.create(prediction)

    def get_prediction_by_id(self, prediction_id: uuid.UUID) -> Prediction | None:
        return self._repository.find_by_id(prediction_id)

    def get_predictions_by_request_id(self, request_id: str) -> List[Prediction]:
        pass

    def get_predictions_by_model_id(self, model_id: str) -> List[Prediction]:
        pass

    def get_all_predictions(
        self, limit: int = 100, offset: int = 0
    ) -> List[Prediction]:
        pass

    def update_prediction(
        self,
        prediction_id: uuid.UUID,
        new_prediction_data: Optional[Dict[str, Any]] = None,
        new_model_id: Optional[str] = None,
    ) -> Prediction:
        pass

    def delete_prediction(self, prediction_id: uuid.UUID) -> bool:
        pass

    def prediction_exists(self, prediction_id: uuid.UUID) -> bool:
        pass
