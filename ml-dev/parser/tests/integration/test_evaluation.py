from parser.infrastructure.evaluator import Evaluator
from parser.infrastructure.parser import MockParser
from parser.infrastructure.storage import LocalStorageService
from parser.service.evaluate import EvaluationService


def test_evaluate():
    EvaluationService.evaluate_model(
        dataset_uri="path/to/dataset",
        parser=MockParser(),
        storage_service=LocalStorageService(),
        evaluation_service=Evaluator(),
    )
