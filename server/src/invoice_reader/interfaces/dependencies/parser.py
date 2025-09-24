from invoice_reader.infrastructure.parser import TestParser
from invoice_reader.services.interfaces.parser import IParser


def get_parser() -> IParser:
    return TestParser()
