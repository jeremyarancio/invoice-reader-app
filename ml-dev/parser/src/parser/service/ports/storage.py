from abc import ABC, abstractmethod

from parser.domain.parse import Annotation


class IStorageService(ABC):
    @abstractmethod
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str
    ) -> None:
        pass

    @abstractmethod
    def load_dataset(self, dataset_uri: str) -> list[Annotation]:
        pass

    @abstractmethod
    def get_document_image(self, image_uri: str):
        raise NotImplementedError
