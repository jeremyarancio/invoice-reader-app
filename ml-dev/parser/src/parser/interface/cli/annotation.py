from typer import Typer

from parser.settings import get_settings
from parser.service.annotation import AnnotationService
from parser.interface import dependencies


settings = get_settings()

app = Typer()


@app.command("create-project")
def create_project(project_name: str, description: str = "") -> None:
    print(f"Creating Label Studio project: {project_name}")
    AnnotationService.create_project(
        project_name=project_name,
        description=description,
        annotation_template_path=settings.label_studio_settings.parser_benchmark_template_path,
        annotation_service=dependencies.get_annotator(
            label_studio_url=settings.label_studio_url,
            label_studio_api_key=settings.label_studio_api_key,
        ),
    )
    print("Project created successfully.")


@app.command("export-annotations")
def export_annotations(
    project_id: int,
    storage_export_path: str = settings.benchmark.benchmark_dataset_s3_path,
) -> None:
    print(f"Exporting annotations for project ID: {project_id}")
    AnnotationService.export_annotations(
        project_id=project_id,
        dataset_uri=storage_export_path,
        storage_repository=dependencies.get_storage_service(
            s3_bucket_name=settings.s3_bucket_name
        ),
        annotation_service=dependencies.get_annotator(
            label_studio_url=settings.label_studio_url,
            label_studio_api_key=settings.label_studio_api_key,
        ),
    )
    print("Annotations exported successfully.")
