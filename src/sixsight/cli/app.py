from pathlib import Path
from urllib.parse import urlparse

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="SixSight — Toronto open data analytics CLI")
DEFAULT_DATA_DIR = Path("data/raw")
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
def info(
    name: str = typer.Argument(..., help="Dataset name or ID"),
    list_files: bool = typer.Option(
        False, "--list", "-l", help="List all resource files with format and last modified date"
    ),
) -> None:
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

    if list_files:
        table = Table("Name", "Format", "Last Modified", title="Resources")
        for r in ds.resources:
            last_modified = r.last_modified.strftime("%Y-%m-%d %H:%M") if r.last_modified else "—"
            table.add_row(r.name, r.format, last_modified)
        console.print(table)


@app.command()
def download(
    name: str = typer.Argument(..., help="Dataset name or ID"),
    fmt: str | None = typer.Option(
        None, "--format", "-f", help="Only download resources of this format (e.g. CSV)"
    ),
    data_dir: Path = typer.Option(
        DEFAULT_DATA_DIR, "--data-dir", help="Root directory for downloads"
    ),
) -> None:
    """Download all resource files for a dataset into data/<name>/."""
    import json

    from sixsight.config import SETTINGS
    from sixsight.ingestion.client import TorontoOpenDataClient
    from sixsight.models.dataset import Resource

    dataset_dir = data_dir / name

    with TorontoOpenDataClient(config=SETTINGS) as client:
        ds = client.get_dataset(name)

        resources = ds.resources
        if fmt:
            resources = [r for r in resources if r.format.upper() == fmt.upper()]

        dataset_dir.mkdir(parents=True, exist_ok=True)

        downloaded = 0
        skipped = 0
        for resource in resources:
            url_path = urlparse(resource.url).path
            ext = f".{resource.format.lower()}" if resource.format else ""
            filename = Path(url_path).name or f"{resource.id}{ext}"
            dest = dataset_dir / filename
            sidecar = dataset_dir / f"{filename}.json"

            if sidecar.exists():
                cached = Resource.model_validate_json(sidecar.read_text())
                if cached.last_modified == resource.last_modified:
                    console.print(f"[dim]skip[/dim]  {resource.name} ({resource.format})")
                    skipped += 1
                    continue

            console.print(f"[bold]fetch[/bold] {resource.name} ({resource.format}) → {dest}")
            client.download_resource(resource, dest)
            sidecar.write_text(json.dumps(resource.model_dump(mode="json"), indent=2))
            downloaded += 1

    console.print(f"\n[green]Done.[/green] {downloaded} downloaded, {skipped} skipped.")
