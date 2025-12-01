from parser.domain.metrics import Metrics
from parser.service.ports.evaluator import IEvaluationService
from parser.service.ports.parser import IParser
from parser.service.ports.storage import IStorageService


class EvaluationService:
    @staticmethod
    def evaluate_model(
        dataset_uri: str,
        parser: IParser,
        storage_service: IStorageService,
        evaluation_service: IEvaluationService,
    ) -> Metrics:
        annotations = storage_service.load_dataset(dataset_uri=dataset_uri)
        images = [
            storage_service.get_document_image(image_uri=annotation.image_uri)
            for annotation in annotations
        ]
        predictions = parser.parse(images=images)
        metrics = evaluation_service.evaluate_parser(
            annotations=annotations, predictions=predictions
        )
        return metrics
