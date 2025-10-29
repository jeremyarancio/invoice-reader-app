from parser.domain.annotation import Annotation
from parser.domain.prediction import Prediction
from parser.service.ports.evaluator import IEvaluator
from parser.domain.metrics import Metrics, FieldMetrics


class Evaluator(IEvaluator):
    EVALUATION_FIELDS = [
        "currency",
        "gross_amount",
        "vat",
        "issued_date",
        "invoice_number",
        "client_name",
        "client_street_address_number",
        "client_street_address",
        "client_city",
        "client_zipcode",
        "client_country",
    ]

    @staticmethod
    def _calculate_field_metrics(
        annotations: list[Annotation], predictions: list[Prediction], field_name: str
    ) -> FieldMetrics:
        """Calculate precision, recall, and F1 for a single field."""
        if len(annotations) != len(predictions):
            raise ValueError(
                f"Number of annotations ({len(annotations)}) must match predictions ({len(predictions)})"
            )

        correct = 0
        total = len(annotations)

        for annotation, prediction in zip(annotations, predictions, strict=True):
            ann_value = getattr(annotation, field_name)
            pred_value = getattr(prediction, field_name)

            if ann_value is None and pred_value is None:
                correct += 1
            elif ann_value is not None and pred_value is not None:
                if isinstance(ann_value, float):
                    if abs(ann_value - pred_value) < 0.01:
                        correct += 1
                elif isinstance(ann_value, str):
                    if ann_value.lower().strip() == pred_value.lower().strip():
                        correct += 1

        precision = correct / total if total > 0 else 0
        recall = precision  # Since total predictions = total annotations
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        return FieldMetrics(precision=precision, recall=recall, f1_score=f1_score)

    def evaluate_parser(
        self, annotations: list[Annotation], predictions: list[Prediction]
    ) -> Metrics:
        field_metrics = {
            field_name: self._calculate_field_metrics(
                annotations, predictions, field_name
            )
            for field_name in self.EVALUATION_FIELDS
        }
        overall_precision = sum(
            field_metric.precision for field_metric in field_metrics.values()
        ) / len(field_metrics)
        overall_recall = sum(
            field_metric.recall for field_metric in field_metrics.values()
        ) / len(field_metrics)
        overall_f1 = sum(
            field_metric.f1_score for field_metric in field_metrics.values()
        ) / len(field_metrics)

        return Metrics(
            overall_precision=overall_precision,
            overall_recall=overall_recall,
            overall_f1_score=overall_f1,
            **field_metrics,
        )
