from enum import Enum

from parser.infrastructure.annotation import LabelStudioAnnotator
from parser.infrastructure.evaluator import Evaluator
from parser.infrastructure.parser import GeminiParser, MockParser
from parser.infrastructure.storage import S3StorageRepository
from parser.service.ports.annotation import IAnnotator
from parser.service.ports.evaluator import IEvaluationService
from parser.service.ports.parser import IParser
from parser.service.ports.storage import IStorageService


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


def get_storage_service(s3_bucket_name: str) -> IStorageService:
    return S3StorageRepository(
        s3_bucket_name=s3_bucket_name,
    )


def get_parser(model: EvaluationModel) -> IParser:
    if model == EvaluationModel.GEMINI_2_5_FLASH:
        return GeminiParser()
    elif model == EvaluationModel.MOCK:
        return MockParser()
    else:
        raise ValueError(f"Unsupported model: {model}")


def get_evaluation_service() -> IEvaluationService:
    return Evaluator()


def get_document_repository() -> IDocumentRepository:
    return S3DocumentRepository()
