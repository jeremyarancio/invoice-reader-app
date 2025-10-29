from abc import ABC, abstractmethod
from PIL.Image import Image

from parser.domain.prediction import Prediction


class IParser(ABC):
    @abstractmethod
    def parse(self, images: list[Image]) -> list[Prediction]:
        pass
