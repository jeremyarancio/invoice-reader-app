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
        print(f"Loading annotated data from {dataset_uri}...")
        annotations = storage_service.load_dataset(dataset_uri=dataset_uri)
        print(f"Loaded {len(annotations)} annotations.")
        print("Loading document images from storage...")
        images = [
            storage_service.get_document_image(image_uri=annotation.image_uri)
            for annotation in annotations
        ]
        print(f"Loaded {len(images)} document images.")
        print("Parsing document images with parser...")
        predictions = parser.parse(images=images)
        print(f"Parsed {len(predictions)} documents.")
        print("Evaluating parser predictions...")
        metrics = evaluation_service.evaluate_parser(
            annotations=annotations, predictions=predictions
        )
        print("Evaluation complete.")
        return metrics
