from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="TTC subway delay analysis commands")
console = Console()

DATASET_NAME = "ttc-subway-delay-data"

# fmt: off
_FILES = [
    "ttc-subway-delay-jan-2014-april-2017.xlsx",
    "ttc-subway-delay-may-december-2017.xlsx",
    "ttc-subway-delay-data-2018.xlsx",
    "ttc-subway-delay-data-2019.xlsx",
    "ttc-subway-delay-2020.xlsx",
    "ttc-subway-delay-2021.xlsx",
    "ttc-subway-delay-2022.xlsx",
    "ttc-subway-delay-2023.xlsx",
    "ttc-subway-delay-2024.xlsx",
    "ttc-subway-delay-data-since-2025.csv",
]
# fmt: on


@app.command()
def aggregate(
    data_dir: Path = typer.Option(Path("data"), "--data-dir", help="Root data directory"),
) -> None:
    """Concatenate all TTC subway delay files and write monthly stats to data/prep."""
    import polars as pl

    from sixsight.transforms.ttc_subway_delay import monthly_by_category, monthly_stats

    raw_dir = data_dir / "raw" / DATASET_NAME
    meta_path = data_dir / "meta" / DATASET_NAME / "codes_categories.csv"
    prep_dir = data_dir / "prep" / DATASET_NAME

    frames: list[pl.DataFrame] = []

    for name in _FILES:
        path = raw_dir / name
        console.print(f"[dim]load[/dim]  {name}")
        if path.suffix == ".csv":
            df = pl.read_csv(path, schema_overrides={"Date": pl.Date})
            frames.append(df.drop("_id"))
        else:
            frames.append(pl.read_excel(path))

    combined = pl.concat(frames)

    prep_dir.mkdir(parents=True, exist_ok=True)

    monthly = monthly_stats(combined)
    monthly_path = prep_dir / "monthly.csv"
    monthly.write_csv(monthly_path)
    console.print(f"[green]✓[/green] {len(monthly)} months → {monthly_path}")

    categories = pl.read_csv(meta_path)
    monthly_cat = monthly_by_category(combined, categories)
    monthly_cat_path = prep_dir / "monthly_by_category.csv"
    monthly_cat.write_csv(monthly_cat_path)
    console.print(f"[green]✓[/green] {len(monthly_cat)} month×category rows → {monthly_cat_path}")
