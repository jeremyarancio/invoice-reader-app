from enum import Enum

from parser.infrastructure.document import S3DocumentRepository
from parser.infrastructure.evaluator import Evaluator
from parser.infrastructure.parser import Gemini2_5FlashParser, MockParser
from parser.infrastructure.storage import S3StorageRepository
from parser.service.ports.document import IDocumentRepository
from parser.service.ports.evaluator import IEvaluator
from parser.service.ports.parser import IParser
from parser.service.ports.storage import IStorageRepository
from parser.settings import get_settings

settings = get_settings()


class EvaluationModel(Enum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GPT_5_TURBO = "gpt-5-turbo"
    NANONETS_OCRs = "nanonets-ocrs"
    MOCK = "mock"


def get_storage_repository() -> IStorageRepository:
    return S3StorageRepository()


def get_parser(model: EvaluationModel) -> IParser:
    if model == EvaluationModel.GEMINI_2_5_FLASH:
        return Gemini2_5FlashParser()
    elif model == EvaluationModel.MOCK:
        return MockParser()
    else:
        raise ValueError(f"Unsupported model: {model}")


def get_evaluator() -> IEvaluator:
    return Evaluator()


def get_document_repository() -> IDocumentRepository:
    return S3DocumentRepository()
