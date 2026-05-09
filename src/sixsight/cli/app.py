import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="SixSight — Toronto open data analytics CLI")
console = Console()


@app.command()
def search(
    query: str = typer.Argument(..., help="Search term"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results"),
) -> None:
    """Search City of Toronto datasets."""
    from sixsight.config import SETTINGS
    from sixsight.ingestion.client import TorontoOpenDataClient

    with TorontoOpenDataClient(config=SETTINGS) as client:
        datasets = client.search_datasets(query, limit=limit)

    table = Table("Name", "Title", "Formats", title=f'Results for "{query}"')
    for ds in datasets:
        formats = ", ".join({r.format for r in ds.resources if r.format})
        table.add_row(ds.name, ds.title, formats)

    console.print(table)


@app.command()
def info(name: str = typer.Argument(..., help="Dataset name or ID")) -> None:
    """Show metadata for a dataset."""
    from sixsight.config import SETTINGS
    from sixsight.ingestion.client import TorontoOpenDataClient

    with TorontoOpenDataClient(config=SETTINGS) as client:
        ds = client.get_dataset(name)

    console.print(f"[bold]{ds.title}[/bold]")
    console.print(f"ID: {ds.id}")
    console.print(f"Org: {ds.organization}")
    console.print(f"Tags: {', '.join(ds.tags)}")
    console.print(f"\n{ds.notes}")
