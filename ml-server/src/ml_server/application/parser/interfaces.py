from abc import ABC, abstractmethod

from PIL.Image import Image


class Parser(ABC):
    @abstractmethod
    def parse(self, image: Image) -> dict:
        pass
