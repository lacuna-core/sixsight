from pathlib import Path
from typing import Protocol

import polars as pl


class Transform(Protocol):
    def __call__(self, df: pl.DataFrame) -> pl.DataFrame: ...


class Pipeline:
    """Composable chain of DataFrame transforms."""

    def __init__(self, steps: list[Transform] | None = None) -> None:
        self._steps: list[Transform] = steps or []

    def pipe(self, step: Transform) -> Pipeline:
        return Pipeline([*self._steps, step])

    def run(self, df: pl.DataFrame) -> pl.DataFrame:
        for step in self._steps:
            df = step(df)
        return df


def load_csv(path: str | Path) -> pl.DataFrame:
    return pl.read_csv(path, infer_schema_length=10_000)


def load_json(path: str | Path) -> pl.DataFrame:
    return pl.read_json(path)
