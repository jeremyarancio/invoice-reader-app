from PIL.Image import Image

from ml_server.application.parser.interfaces import Parser


class ParserService:
    def __init__(self, parser: Parser):
        self.parser = parser

    def parse(self, image: Image) -> dict:
        structured_output = self.parser.parse(image=image)
        return structured_output