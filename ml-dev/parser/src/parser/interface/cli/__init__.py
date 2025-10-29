from typer import Typer

from parser.interface.cli import label_studio
from parser.interface.cli import evaluate

app = Typer()

app.add_typer(label_studio.app, name="label-studio")
app.add_typer(evaluate.app, name="evaluate")
