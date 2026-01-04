from parser.infrastructure.annotation import MockAnnotator
from parser.infrastructure.storage import LocalStorageService
from parser.service.annotation import AnnotationService


def test_export_annotation():
    AnnotationService.export_annotations(
        project_id=1,
        dataset_uri="tests/data/exports",
        annotation_service=MockAnnotator(),
        storage_repository=LocalStorageService(),
    )
