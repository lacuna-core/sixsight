import polars as pl
from great_tables import GT


def summary_table(df: pl.DataFrame, *, title: str = "") -> GT:
    return GT(df.to_pandas()).tab_header(title=title)
