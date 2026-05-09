import typer
from rich.console import Console

app = typer.Typer(help="TTC subway delay analysis commands")
console = Console()


@app.command()
def aggregate() -> None:
    """Aggregate subway delay data."""
    console.print("Not implemented yet.")
