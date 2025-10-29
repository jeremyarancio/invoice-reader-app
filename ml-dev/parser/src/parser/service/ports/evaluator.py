from abc import ABC, abstractmethod

from parser.domain.annotation import Annotation
from parser.domain.metrics import Metrics
from parser.domain.prediction import Prediction


class IEvaluator(ABC):
    @abstractmethod
    def evaluate_parser(
        self, annotations: list[Annotation], predictions: list[Prediction]
    ) -> Metrics:
        pass
