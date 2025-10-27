from label_studio_sdk import LabelStudio

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
