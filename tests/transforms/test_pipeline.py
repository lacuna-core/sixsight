import polars as pl

from sixsight.transforms.pipeline import Pipeline


def test_pipeline_identity() -> None:
    df = pl.DataFrame({"a": [1, 2, 3]})
    result = Pipeline().run(df)
    assert result.equals(df)


def test_pipeline_chaining() -> None:
    df = pl.DataFrame({"a": [1, 2, 3]})

    def double(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns(pl.col("a") * 2)

    result = Pipeline().pipe(double).run(df)
    assert result["a"].to_list() == [2, 4, 6]
