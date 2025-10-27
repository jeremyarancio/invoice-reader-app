from typer import Typer

from parser.service.label_studio import LabelStudioService

app = Typer()


@app.command("create-project")
def create_project(project_name: str, description: str = "") -> None:
    print(f"Creating Label Studio project: {project_name}")
    LabelStudioService.create_project(
        project_name=project_name, description=description
    )
    print("Project created successfully.")