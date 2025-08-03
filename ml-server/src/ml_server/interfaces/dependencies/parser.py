from ml_server.infrastructure.parser import ParserInteface, vLLMParser


def get_parser() -> ParserInteface:
    """Factory function to create and inject an instance of vLLMParser."""
    return vLLMParser()
