from typer import Typer

from parser.interface.cli import label_studio

app = Typer()

app.add_typer(label_studio.app, name="label-studio")
