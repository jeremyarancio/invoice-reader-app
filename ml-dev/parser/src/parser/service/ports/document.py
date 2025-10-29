from abc import ABC, abstractmethod
from PIL.Image import Image


class IDocumentRepository(ABC):
    @abstractmethod
    def get_document_image(self, image_name: str) -> Image:
        pass
