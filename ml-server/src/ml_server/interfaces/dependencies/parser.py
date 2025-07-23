from ml_server.infrastructure.models.parser import NanonetsOCRParser


def get_parser(model, tokenizer, processor) -> NanonetsOCRParser:
    """Factory function to create an instance of NanonetsOCRParser."""
    return NanonetsOCRParser(model=model, tokenizer=tokenizer, processor=processor)
