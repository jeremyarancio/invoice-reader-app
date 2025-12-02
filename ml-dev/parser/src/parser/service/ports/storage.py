from abc import ABC, abstractmethod
from pathlib import Path

from parser.domain.parse import Annotation


class IStorageService(ABC):
    @abstractmethod
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str | Path
    ) -> None:
        pass

    @abstractmethod
    def load_dataset(self, dataset_uri: str | Path) -> list[Annotation]:
        pass

    @abstractmethod
    def get_document_image(self, image_uri: str):
        raise NotImplementedError
