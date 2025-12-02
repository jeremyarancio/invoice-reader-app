from abc import ABC, abstractmethod

from parser.domain.parse import Annotation, Prediction
from parser.domain.metrics import Metrics


class IEvaluationService(ABC):
    @classmethod
    @abstractmethod
    def evaluate_parser(
        cls, annotations: list[Annotation], predictions: list[Prediction]
    ) -> Metrics:
        raise NotImplementedError
