from parser.infrastructure.annotation import MockAnnotator
from parser.infrastructure.storage import InMemoryStorageRepository
from parser.service.annotation import AnnotationService


InMemoryStorageRepository.init_memory()


def test_export_annotation():
    AnnotationService.export_annotations(
        project_id=1,
        dataset_uri="tests/data/exports",
        annotation_service=MockAnnotator(),
        storage_repository=InMemoryStorageRepository(),
    )
