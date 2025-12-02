from difflib import SequenceMatcher


from parser.domain.parse import Annotation, Prediction, ParsedData
from parser.service.ports.evaluator import IEvaluationService
from parser.domain.metrics import Metrics, FieldMetrics


class Evaluator(IEvaluationService):
    @staticmethod
    def _calculate_float(ann_value: float, pred_value: float) -> bool:
        return abs(ann_value - pred_value) < 1

    @staticmethod
    def _calculate_str(ann_value: str, pred_value: str, threshold: float = 0.8) -> bool:
        """
        Compare strings using similarity ratio.
        threshold: minimum similarity score (0-1) to consider a match
        """
        ann_normalized = ann_value.lower().strip()
        pred_normalized = pred_value.lower().strip()

        # Calculate similarity ratio (0-1, where 1 is identical)
        similarity = SequenceMatcher(None, ann_normalized, pred_normalized).ratio()
        return similarity >= threshold

    @classmethod
    def _calculate_field_metrics(
        cls,
        annotations: list[Annotation],
        predictions: list[Prediction],
        field_name: str,
    ) -> FieldMetrics:
        """Calculate precision, recall, and F1 for a single field."""
        if len(annotations) != len(predictions):
            raise ValueError(
                f"Number of annotations ({len(annotations)}) must match predictions ({len(predictions)})"
            )
        if not annotations:
            raise ValueError("No annotations provided for evaluation.")

        correct = 0
        total = len(annotations)

        for annotation, prediction in zip(annotations, predictions, strict=True):
            # Extract field values from the ParsedData objects
            ann_value = getattr(annotation.data, field_name)
            pred_value = getattr(prediction.data, field_name)

            if ann_value is None and pred_value is None:
                correct += 1
            elif ann_value is not None and pred_value is not None:
                if isinstance(ann_value, float):
                    if cls._calculate_float(ann_value, pred_value):
                        correct += 1
                elif isinstance(ann_value, str):
                    if cls._calculate_str(ann_value, pred_value):
                        correct += 1
                else:
                    if ann_value == pred_value:
                        correct += 1

        precision = correct / total if total > 0 else 0
        recall = precision  # Since total predictions = total annotations
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )
        return FieldMetrics(
            name=field_name,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
        )

    @classmethod
    def evaluate_parser(
        cls, annotations: list[Annotation], predictions: list[Prediction]
    ) -> Metrics:
        fields = ParsedData.model_fields.keys()

        field_metrics = [
            cls._calculate_field_metrics(annotations, predictions, field_name)
            for field_name in fields
        ]

        overall_precision = sum(
            field_metric.precision for field_metric in field_metrics
        ) / len(field_metrics)
        overall_recall = sum(
            field_metric.recall for field_metric in field_metrics
        ) / len(field_metrics)
        overall_f1 = sum(field_metric.f1_score for field_metric in field_metrics) / len(
            field_metrics
        )

        return Metrics(
            overall_precision=overall_precision,
            overall_recall=overall_recall,
            overall_f1_score=overall_f1,
            field_metrics=field_metrics,
        )
