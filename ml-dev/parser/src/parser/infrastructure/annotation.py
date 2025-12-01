import json
from pathlib import Path

from label_studio_sdk import LabelStudio

from parser.domain.parse import Annotation
from parser.infrastructure.schemas.label_studio import LabelStudioExportJSONMIN
from parser.service.ports.annotation import IAnnotator


class MockAnnotator(IAnnotator):
    def create_project(
        self,
        project_name: str,
        description: str,
        annotation_template_path: Path,
    ) -> None:
        """Mock create project - does nothing."""
        pass

    def export_annotations(self, project_id: int) -> list[Annotation]:
        """Mock export annotations - returns empty list."""
        return []


class LabelStudioAnnotator(IAnnotator):
    def __init__(
        self,
        label_studio_url: str,
        label_studio_api_key: str,
    ) -> None:
        self.label_studio_url = label_studio_url
        self.label_studio_api_key = label_studio_api_key

    def create_project(
        self,
        project_name: str,
        description: str,
        annotation_template_path: Path,
    ) -> None:
        """Create a Label Studio project based on the XML template."""
        with open(annotation_template_path, "r") as f:
            label_config = f.read()
        client = LabelStudio(
            base_url=self.label_studio_url,
            api_key=self.label_studio_api_key,
        )
        client.projects.create(
            title=project_name,
            description=description,
            label_config=label_config,
        )

    def export_annotations(self, project_id: int) -> list[Annotation]:
        """Export annotations from Label Studio.
        Docs: https://api.labelstud.io/tutorials/tutorials/export-and-convert-snapshots
        """
        client = LabelStudio(
            base_url=self.label_studio_url,
            api_key=self.label_studio_api_key,
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
            LabelStudioExportJSONMIN.model_validate(data).to_annotation()
            for data in json.loads(annotations_data.decode("utf-8"))
        ]
        return annotations
