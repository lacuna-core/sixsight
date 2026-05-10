import polars as pl
import pytest

from sixsight.transforms.ttc_subway_delay import monthly_by_category


@pytest.fixture
def categories() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "CODE": ["EUDO", "SUDP", "MUATC"],
            "CATEGORY": ["Mechanical/Vehicle", "Patron", "Mechanical/Infrastructure"],
        }
    )


@pytest.fixture
def raw() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "Date": pl.Series(
                [
                    "2025-01-10",
                    "2025-01-15",
                    "2025-01-20",
                    "2025-02-05",
                    "2025-02-10",
                    "2025-02-15",
                ],
                dtype=pl.Date,
            ),
            "Code": ["EUDO", "EUDO", "SUDP", "MUATC", "SUDP", "UNKNOWN"],
            "Min Delay": [5, 25, 30, 10, 20, 15],
        }
    )


def test_output_columns(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    assert result.columns == [
        "year_month",
        "month_label",
        "category",
        "delays",
        "total_delay",
        "major_delays",
    ]


def test_sorted_by_year_month_then_category(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    assert result["year_month"].to_list() == sorted(result["year_month"].to_list())
    jan = result.filter(pl.col("year_month") == 202501)
    assert jan["category"].to_list() == sorted(jan["category"].to_list())


def test_month_label(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    labels = result.filter(pl.col("year_month") == 202501)["month_label"].unique()
    assert labels.to_list() == ["Jan 2025"]


def test_delays_count(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    jan_mech = result.filter(
        (pl.col("year_month") == 202501) & (pl.col("category") == "Mechanical/Vehicle")
    )
    assert jan_mech["delays"].item() == 2


def test_total_delay(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    jan_mech = result.filter(
        (pl.col("year_month") == 202501) & (pl.col("category") == "Mechanical/Vehicle")
    )
    assert jan_mech["total_delay"].item() == 30  # 5 + 25


def test_major_delays(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    # EUDO jan: delays 5, 25 → 1 major; SUDP jan: delay 30 → 1 major
    result = monthly_by_category(raw, categories)
    jan_mech = result.filter(
        (pl.col("year_month") == 202501) & (pl.col("category") == "Mechanical/Vehicle")
    )
    assert jan_mech["major_delays"].item() == 1

    jan_patron = result.filter((pl.col("year_month") == 202501) & (pl.col("category") == "Patron"))
    assert jan_patron["major_delays"].item() == 1


def test_unknown_code_collapsed_to_other(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    # UNKNOWN code has no lookup entry → Other; MUATC is Mechanical/Infrastructure → major
    feb_other = result.filter((pl.col("year_month") == 202502) & (pl.col("category") == "Other"))
    assert feb_other["delays"].item() == 1
    assert feb_other["total_delay"].item() == 15


def test_non_major_known_category_collapsed_to_other(categories: pl.DataFrame) -> None:
    raw_non_major = pl.DataFrame(
        {
            "Date": pl.Series(["2025-03-01"], dtype=pl.Date),
            "Code": ["ZZNM"],
            "Min Delay": [10],
        }
    )
    cats_with_non_major = pl.concat(
        [
            categories,
            pl.DataFrame({"CODE": ["ZZNM"], "CATEGORY": ["Planned Work"]}),
        ]
    )
    result = monthly_by_category(raw_non_major, cats_with_non_major)
    assert result["category"].item() == "Other"


def test_no_rows_dropped(raw: pl.DataFrame, categories: pl.DataFrame) -> None:
    result = monthly_by_category(raw, categories)
    assert result["delays"].sum() == len(raw)
