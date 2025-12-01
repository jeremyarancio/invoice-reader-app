from enum import Enum

from parser.infrastructure.annotation import LabelStudioAnnotator
from parser.infrastructure.document import S3DocumentRepository
from parser.infrastructure.evaluator import Evaluator
from parser.infrastructure.parser import Gemini2_5FlashParser, MockParser
from parser.infrastructure.storage import S3StorageRepository
from parser.service.ports.annotation import IAnnotator
from parser.service.ports.document import IDocumentRepository
from parser.service.ports.evaluator import IEvaluator
from parser.service.ports.parser import IParser
from parser.service.ports.storage import IStorageRepository


class EvaluationModel(Enum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GPT_5_TURBO = "gpt-5-turbo"
    NANONETS_OCRs = "nanonets-ocrs"
    MOCK = "mock"


def get_annotator(
    label_studio_url: str,
    label_studio_api_key: str,
) -> IAnnotator:
    return LabelStudioAnnotator(
        label_studio_url=label_studio_url,
        label_studio_api_key=label_studio_api_key,
    )


def get_storage_repository(s3_bucket_name: str) -> IStorageRepository:
    return S3StorageRepository(
        s3_bucket_name=s3_bucket_name,
    )


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
