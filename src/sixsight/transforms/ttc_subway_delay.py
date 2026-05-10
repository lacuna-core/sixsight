import polars as pl

MAJOR_DELAY_THRESHOLD = 20

MAJOR_CATEGORIES: frozenset[str] = frozenset(
    {
        "Mechanical/Infrastructure",
        "Mechanical/Vehicle",
        "Operational/Process",
        "Patron",
        "Security",
        "Weather",
    }
)


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
            (pl.col("Min Delay") >= MAJOR_DELAY_THRESHOLD).sum().alias("major_delays"),
        )
        .sort("year_month")
    )


def monthly_by_category(df: pl.DataFrame, categories: pl.DataFrame) -> pl.DataFrame:
    """Aggregate TTC subway delay data into monthly stats per delay-code category.

    Input columns for df (from the TTC open data CSV):
        Date      (Date)   — incident date
        Code      (Utf8)   — TTC delay code
        Min Delay (Int64)  — delay duration in minutes

    Input columns for categories (from data/meta/ttc-subway-delay-data/codes_categories.csv):
        CODE      (Utf8)   — delay code, joined to df.Code
        CATEGORY  (Utf8)   — high-level category label

    Codes absent from the categories lookup are assigned "Other".
    Categories not in MAJOR_CATEGORIES are collapsed into "Other".

    Output columns:
        year_month   (Int32)  — sortable YYYYMM integer (e.g. 202503)
        month_label  (Utf8)   — human-readable label (e.g. "Mar 2025")
        category     (Utf8)   — major category label, or "Other"
        delays       (UInt32) — total number of delay incidents
        total_delay  (Int64)  — sum of Min Delay in minutes
        major_delays (UInt32) — count of incidents with Min Delay >= 20 minutes

    Rows are sorted ascending by year_month then category.
    """
    major = list(MAJOR_CATEGORIES)
    return (
        df.join(
            categories.select(["CODE", "CATEGORY"]),
            left_on="Code",
            right_on="CODE",
            how="left",
        )
        .with_columns(
            pl.when(pl.col("CATEGORY").is_in(major))
            .then(pl.col("CATEGORY"))
            .otherwise(pl.lit("Other"))
            .alias("category"),
            (pl.col("Date").dt.year() * 100 + pl.col("Date").dt.month()).alias("year_month"),
            pl.col("Date").dt.strftime("%b %Y").alias("month_label"),
        )
        .group_by(["year_month", "month_label", "category"])
        .agg(
            pl.len().alias("delays"),
            pl.col("Min Delay").sum().alias("total_delay"),
            (pl.col("Min Delay") >= MAJOR_DELAY_THRESHOLD).sum().alias("major_delays"),
        )
        .sort(["year_month", "category"])
    )
