from pathlib import Path

from parser.service.ports.annotation import IAnnotator
from parser.service.ports.storage import IStorageRepository
from parser.settings import get_settings

settings = get_settings()


class AnnotationService:
    @staticmethod
    def create_project(
        project_name: str,
        description: str,
        annotation_template_path: Path,
        annotation_service: IAnnotator,
    ) -> None:
        annotation_service.create_project(
            project_name=project_name,
            description=description,
            annotation_template_path=annotation_template_path,
        )

    @staticmethod
    def export_annotations(
        project_id: int,
        dataset_uri: str,
        storage_repository: IStorageRepository,
        annotation_service: IAnnotator,
    ) -> None:
        annotations = annotation_service.export_annotations(project_id=project_id)
        storage_repository.export_to_dataset(
            annotations=annotations, dataset_uri=dataset_uri
        )
