import polars as pl


def monthly_stats(df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate TTC subway delay data into total and max delay per calendar month.

    Input columns (from the TTC open data CSV):
        Date      (Utf8)   — incident date, format "YYYY-MM-DD"
        Min Delay (Int64)  — delay duration in minutes

    Output columns:
        year_month  (Int32)  — sortable YYYYMM integer (e.g. 202503)
        month_label (Utf8)   — human-readable label (e.g. "Mar 2025")
        total_delay (Int64)  — sum of Min Delay for the month, in minutes
        max_delay   (Int64)  — largest single Min Delay in the month, in minutes

    Rows are sorted ascending by year_month.
    """
    return (
        df.with_columns(pl.col("Date").str.to_date("%Y-%m-%d"))
        .with_columns(
            (pl.col("Date").dt.year() * 100 + pl.col("Date").dt.month()).alias("year_month"),
            pl.col("Date").dt.strftime("%b %Y").alias("month_label"),
        )
        .group_by(["year_month", "month_label"])
        .agg(
            pl.col("Min Delay").sum().alias("total_delay"),
            pl.col("Min Delay").max().alias("max_delay"),
        )
        .sort("year_month")
    )
