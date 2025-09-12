from invoice_reader.infrastructure.parser import MLServerParser
from invoice_reader.services.interfaces.parser import IParser


def get_parser() -> IParser:
    return MLServerParser()
