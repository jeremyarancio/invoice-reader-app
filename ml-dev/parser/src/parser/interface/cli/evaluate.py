from typer import Typer

from parser.service.evaluate import EvaluateService
from parser.settings import get_settings
from parser.interface import dependencies

settings = get_settings()

app = Typer()


@app.command("evaluate")
def evaluate(model: dependencies.EvaluationModel) -> None:
    metrics = EvaluateService.evaluate_model(
        parser=dependencies.get_parser(model=model),
        storage_repository=dependencies.get_storage_repository(),
        document_repository=dependencies.get_document_repository(),
        evaluator=dependencies.get_evaluator(),
    )
    print("Metrics: ", metrics.model_dump())


# evaluate(model=dependencies.EvaluationModel.GEMINI_2_5_FLASH)
