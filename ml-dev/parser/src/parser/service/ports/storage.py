from abc import ABC, abstractmethod

from parser.domain.annotation import Annotation


class IStorageRepository(ABC):
    @abstractmethod
    def save_annotations(self, annotations: list[Annotation], save_path: str) -> None:
        pass

    @abstractmethod
    def load_annotations(self) -> list[Annotation]:
        pass
