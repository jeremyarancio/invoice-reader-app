from abc import ABC, abstractmethod
from PIL import Image

from parser.domain.parse import Prediction


class IParser(ABC):
    @abstractmethod
    def parse(self, images: list[Image.Image]) -> list[Prediction]:
        raise NotImplementedError
