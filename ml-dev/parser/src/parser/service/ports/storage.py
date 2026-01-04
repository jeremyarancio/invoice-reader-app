from abc import ABC, abstractmethod
from pathlib import Path

from parser.domain.parse import Annotation, Prediction


class IStorageService(ABC):
    @abstractmethod
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str | Path
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_dataset(self, dataset_uri: str | Path) -> list[Annotation]:
        raise NotImplementedError

    @abstractmethod
    def get_document_image(self, image_uri: str):
        raise NotImplementedError

    @abstractmethod
    def save_predictions(
        self,
        evaluation_uri: str,
        annotations: list[Annotation],
        predictions: list[Prediction],
    ) -> None:
        raise NotImplementedError
