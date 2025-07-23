"""Domain exceptions for Prediction aggregate."""

class PredictionException(Exception):
    """Base exception for Prediction domain."""
    pass


class InvalidPredictionError(PredictionException):
    """Exception raised when prediction data is invalid."""

    def __init__(self, message: str):
        super().__init__(f"Invalid prediction data: {message}")
