from typer import Typer

from parser.interface.cli import annotation
from parser.interface.cli import evaluate

app = Typer()

app.add_typer(annotation.app, name="ls")
app.add_typer(evaluate.app, name="eval")
