from invoice_reader.infrastructure.parser import MLServerParser
from invoice_reader.services.interfaces.parser import IParser
from invoice_reader.settings import get_settings

settings = get_settings()


def get_parser() -> IParser:
    return MLServerParser(
        parser_endpoint_url=settings.parser_endpoint_url,
    )
