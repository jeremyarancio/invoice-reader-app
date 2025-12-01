from abc import ABC, abstractmethod
from pathlib import Path

from parser.domain.annotation import Annotation


class IAnnotator(ABC):
    @abstractmethod
    def create_project(
        self,
        project_name: str,
        description: str,
        annotation_template_path: Path,
    ) -> None:
        pass

    @abstractmethod
    def export_annotations(self, project_id: int) -> list[Annotation]:
        pass
