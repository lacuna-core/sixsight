# CLAUDE.md

## Commands

```bash
uv sync --dev                        # install all dependencies
uv run pre-commit install            # wire up git hooks (once per clone)

uv run pytest                        # run all tests with coverage
uv run pytest tests/ingestion/       # run a single test directory
uv run pytest -k test_parse_dataset  # run a single test by name

uv run ruff check                    # lint (src/ and tests/)
uv run ruff check --fix              # lint with auto-fix
uv run ruff format                   # format
uv run mypy                          # type-check (strict, src/ and tests/)

uv run sixsight --help               # run the CLI
```

## Architecture

`src/sixsight/` follows a layered structure:

- **`config.py`** — frozen `Settings` (pydantic-settings, `SIXSIGHT_` env prefix). Calls `load_dotenv()` at import time. The singleton `SETTINGS` is imported by the CLI and passed explicitly to clients — nothing reads `SETTINGS` internally.
- **`ingestion/client.py`** — `TorontoOpenDataClient` takes a `Settings` instance in its constructor (no default). All HTTP goes through the private `_get()` method, which logs the full URL+params at DEBUG level via loguru before sending.
- **`models/dataset.py`** — Pydantic v2 models (`Dataset`, `Resource`) representing CKAN API responses.
- **`transforms/pipeline.py`** — composable `Pipeline` of `Transform` callables operating on `polars.DataFrame`.
- **`viz/charts.py`** — thin wrappers over `great_tables` for tabular output.
- **`cli/app.py`** — Typer CLI (`search`, `info`, `download` commands).

Logging is configured once in `__init__.py`: loguru handler removed and re-added with the level from `SETTINGS.log_level`. Set `SIXSIGHT_LOG_LEVEL=DEBUG` to see outbound HTTP requests.

## Dependencies
Uses [CKAN API](https://docs.ckan.org/en/latest/api/index.html) to access the data

## Key conventions

- Dependency injection: `TorontoOpenDataClient(config=SETTINGS)` — always pass config explicitly, never use the global inside library code.
- Raw JSON from the API is typed `dict[str, Any]`; use `object` only when values won't be accessed.
- mypy is strict. All functions including tests need return type annotations.
- Git hooks (pre-commit) run ruff (fix + format) and mypy on every commit.
- CLI lazy imports: in `cli/app.py`, `sixsight.*` imports must be inside the command function body, not at module level. `typer`, `rich`, and stdlib belong at the top of the file. This keeps `--help` fast and isolates heavy deps per command.
