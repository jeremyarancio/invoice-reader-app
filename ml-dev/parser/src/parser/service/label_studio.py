import json

from label_studio_sdk import LabelStudio

from parser.domain.annotation import Annotation
from parser.service.ports.storage import IStorageRepository
from parser.settings import get_settings

settings = get_settings()

LABEL_STUDIO_TEMPLATE_PATH = {
    "benchmark": settings.label_studio_template_dir / "parser_benchmark.xml",
}


class LabelStudioService:
    @staticmethod
    def create_project(project_name: str, description: str) -> None:
        with open(LABEL_STUDIO_TEMPLATE_PATH["benchmark"], "r") as f:
            label_config = f.read()

        client = LabelStudio(
            base_url=settings.label_studio_url,
            api_key=settings.label_studio_api_key,
        )
        client.projects.create(
            title=project_name,
            description=description,
            label_config=label_config,
        )

    @staticmethod
    def export_annotations(
        project_id: int,
        export_path: str,
        storage_repository: IStorageRepository,
    ) -> None:
        """Docs: https://api.labelstud.io/tutorials/tutorials/export-and-convert-snapshots"""
        client = LabelStudio(
            base_url=settings.label_studio_url,
            api_key=settings.label_studio_api_key,
        )
        # To get more configuration such as JSON_MIN export, the export job should be processed in background
        export_job = client.projects.exports.create(id=project_id)
        # Export in chunks of byte strings
        annotation_chunks = client.projects.exports.download(
            id=project_id, export_type="JSON_MIN", export_pk=export_job.id
        )
        # Convert generator of byte strings to list[dict]
        annotations_data = b"".join(annotation_chunks)
        annotations = [
            Annotation.from_label_studio(data)
            for data in json.loads(annotations_data.decode("utf-8"))
        ]
        storage_repository.save_annotations(
            annotations=annotations, save_path=export_path
        )
