from parser.domain.metrics import Metrics
from parser.service.ports.document import IDocumentRepository
from parser.service.ports.evaluator import IEvaluator
from parser.service.ports.parser import IParser
from parser.service.ports.storage import IStorageRepository


class EvaluateService:
    @staticmethod
    def evaluate_model(
        parser: IParser,
        storage_repository: IStorageRepository,
        document_repository: IDocumentRepository,
        evaluator: IEvaluator,
    ) -> Metrics:
        annotations = storage_repository.load_annotations()
        images = [
            document_repository.get_document_image(image_name=annotation.image_name)
            for annotation in annotations
        ]
        predictions = parser.parse(images=images)
        metrics = evaluator.evaluate_parser(
            annotations=annotations, predictions=predictions
        )
        return metrics
