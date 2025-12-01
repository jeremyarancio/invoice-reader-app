from abc import ABC, abstractmethod

from parser.domain.annotation import Annotation


class IStorageRepository(ABC):
    @abstractmethod
    def export_to_dataset(
        self, annotations: list[Annotation], dataset_uri: str
    ) -> None:
        pass

    @abstractmethod
    def load_from_dataset(self, dataset_uri: str) -> list[Annotation]:
        pass
