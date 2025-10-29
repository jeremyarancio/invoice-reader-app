from typer import Typer

from parser.settings import get_settings
from parser.service.label_studio import LabelStudioService
from parser.interface import dependencies


settings = get_settings()

app = Typer()


@app.command("create-project")
def create_project(project_name: str, description: str = "") -> None:
    print(f"Creating Label Studio project: {project_name}")
    LabelStudioService.create_project(
        project_name=project_name, description=description
    )
    print("Project created successfully.")


@app.command("export-annotations")
def export_annotations(
    project_id: int, export_path: str = settings.benchmark_s3_path
) -> None:
    print(f"Exporting annotations for project ID: {project_id}")
    LabelStudioService.export_annotations(
        project_id=project_id,
        export_path=export_path,
        storage_repository=dependencies.get_storage_repository(),
    )
    print("Annotations exported successfully.")
