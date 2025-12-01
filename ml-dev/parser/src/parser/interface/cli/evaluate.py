from typer import Typer

from parser.service.evaluate import EvaluationService
from parser.settings import get_settings
from parser.interface import dependencies

settings = get_settings()

app = Typer()


@app.command("evaluate")
def evaluate(model: dependencies.EvaluationModel) -> None:
    metrics = EvaluationService.evaluate_model(
        dataset_uri=settings.benchmark.benchmark_dataset_s3_path,
        parser=dependencies.get_parser(model=model),
        storage_service=dependencies.get_storage_service(
            s3_bucket_name=settings.s3_bucket_name
        ),
        evaluation_service=dependencies.get_evaluation_service(),
    )
    print("Metrics: ", metrics.model_dump())
