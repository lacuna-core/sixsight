Analyse a raw dataset and produce a Jupyter notebook with schema overview, aggregations, and key visualisations.

Dataset argument: $ARGUMENTS

## Steps

### 1. Discover the data

- List all files in `data/raw/$1/`.
- For each file that is NOT a `.json` sidecar, read its paired `.json` sidecar to get metadata (format, size, last_modified).
- Identify the primary data file(s) to analyse — prefer CSV. If multiple CSVs exist, use all of them but note their differences.

### 2. Sample and profile

- Read the first ~20 rows and all column headers from each data file.
- For each column collect: dtype, non-null count, and a sample of distinct values (use bash/python one-liners — do NOT load the full file yet).
- Count total rows.
- Identify the key dimensions: date/time columns, categorical columns, numeric columns, geographic columns.
- Form an opinion on which 5–8 questions a member of the public would find most interesting about this data (e.g. trends over time, severity, geography, seasonality, vulnerable groups).

### 3. Create the notebook

Create `notebooks/<dataset>_analysis.ipynb` where `<dataset>` is `$1`.

Use Python's `json` module to write the notebook file directly (as in the existing `notebooks/traffic_collision_analysis.ipynb`) so escaping is handled correctly — do NOT write raw JSON by hand.

#### Notebook structure

Follow the conventions of `notebooks/traffic_collision_analysis.ipynb`:

- **Imports cell**: `from pathlib import Path`, `import polars as pl`, `import altair as alt`
- **Load & Schema section**: read the CSV with `pl.read_csv`, cast columns to appropriate types, print row/column counts, show a schema/null-coverage summary table
- **One section per analytical question** (aim for 8–12 sections), each with:
  - A markdown cell with a `##` heading and 1–2 sentences of context
  - A code cell that computes the aggregation with polars
  - A code cell (or combined) that renders an Altair chart
- **Final heatmap or cross-tab** if two categorical dimensions make sense together

#### Coding conventions

- Use `polars` for all data manipulation — no pandas.
- Use `altair` for all charts — no matplotlib/seaborn.
- Filter out partial years (e.g. the current year if data runs through present) before computing year-level comparisons — add a comment explaining which year is excluded and why.
- Drop or filter rows with obviously invalid values (e.g. lat/lon = 0, null keys) — note the drop count.
- Cast YES/NO string columns to booleans with `pl.col(c).eq("YES")`.
- For time series over many months, sort by a `year_month` string key (`"YYYY-MM"` format) and pass `sort=ym_order` to Altair's X encoding.
- Chart widths: single charts 600–800 px, side-by-side charts 400 px each.
- Use `alt.vconcat(...).properties(spacing=10)` to stack related charts vertically.
- Choose colour palette from: `#4C72B0` (blue), `#C44E52` (red), `#DD8452` (orange), `#55A868` (green), `#8172B3` (purple).
- No comments unless the WHY is non-obvious.

#### Chart ideas (adapt to what the data actually contains)

- Year-over-year totals (bar)
- Monthly seasonality — overall and for the most affected sub-group (bar)
- Day-of-week breakdown (bar, side-by-side with a severity variant)
- Hour-of-day distribution (bar, stacked or faceted if a second dimension is useful)
- Severity / outcome breakdown (horizontal bar, sorted descending)
- Trend for the most vulnerable or socially relevant sub-group (line with points)
- Top 20 geographic areas by volume (horizontal bar)
- Rate metric for geographic areas (e.g. fatality rate per 1 000 incidents) — filter to areas with enough data to be statistically meaningful (>=500 records)
- A notable event or policy change visible in the data (e.g. COVID drop) shown as a monthly time-series
- Heatmap of two categorical dimensions (e.g. hour × day-of-week)

### 4. Smoke-test

After writing the notebook, run the following to confirm it executes without error:

```
uv run jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=120 \
    notebooks/<dataset>_analysis.ipynb --output /tmp/<dataset>_test.ipynb 2>&1 | tail -5
```

If it fails, read the error, fix the notebook, and re-run until it passes.

### 5. Report back

Tell the user:
- Path to the notebook
- How many sections it contains
- The 5–8 analytical questions it answers, as bullet points
- Any data quality issues found (e.g. % of rows with missing coordinates)
