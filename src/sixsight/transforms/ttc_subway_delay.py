import polars as pl


def monthly_stats(df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate TTC subway delay data into total and max delay per calendar month.

    Input columns (from the TTC open data CSV):
        Date      (Date)   — incident date
        Min Delay (Int64)  — delay duration in minutes

    Output columns:
        year_month  (Int32)  — sortable YYYYMM integer (e.g. 202503)
        month_label (Utf8)   — human-readable label (e.g. "Mar 2025")
        delays        (UInt32) — total number of delay incidents in the month
        total_delay   (Int64)  — sum of Min Delay for the month, in minutes
        max_delay     (Int64)  — largest single Min Delay in the month, in minutes
        major_delays  (UInt32) — count of incidents with Min Delay >= 20 minutes

    Rows are sorted ascending by year_month.
    """
    return (
        df.with_columns(
            (pl.col("Date").dt.year() * 100 + pl.col("Date").dt.month()).alias("year_month"),
            pl.col("Date").dt.strftime("%b %Y").alias("month_label"),
        )
        .group_by(["year_month", "month_label"])
        .agg(
            pl.len().alias("delays"),
            pl.col("Min Delay").sum().alias("total_delay"),
            pl.col("Min Delay").max().alias("max_delay"),
            (pl.col("Min Delay") >= 20).sum().alias("major_delays"),
        )
        .sort("year_month")
    )
