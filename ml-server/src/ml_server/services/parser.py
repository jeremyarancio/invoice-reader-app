from typing import BinaryIO

from ml_server.domain.parser import ParserPrediction
from ml_server.services.exceptions import FileFormatNotHandledException
from ml_server.services.ports.parser import IParser
from ml_server.utils.logger import get_logger

logger = get_logger()


class ParserService:
    @staticmethod
    def parse(
        file: BinaryIO, content_type: str, parser: IParser, allowed_formats: list[str]
    ) -> ParserPrediction:
        if content_type not in allowed_formats:
            raise FileFormatNotHandledException(f"Unsupported content type: {content_type}")
        logger.info("Starting invoice parsing")
        parsed_data = parser.parse(file)
        logger.info("Invoice parsing completed successfully")
        return parsed_data
