from ml_server.infrastructure.parser import GeminiParser
from ml_server.services.ports.parser import IParser
from ml_server.settings import get_settings

settings = get_settings()


def get_parser(
    api_key: str = settings.gemini_api_key,
    model_name: str = settings.parser_config.model_name,
) -> IParser:
    """Factory function to create and inject an instance of GeminiParser."""
    return GeminiParser(
        api_key=api_key,
        model_name=model_name,
    )
