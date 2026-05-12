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
- **`cli/app.py`** — Typer CLI (`search`, `info`, `download` commands). Sub-command groups live in separate files (e.g. `cli/ttc_subway_delay.py`) and are registered via `app.add_typer(...)`.

Logging is configured once in `__init__.py`: loguru handler removed and re-added with the level from `SETTINGS.log_level`. Set `SIXSIGHT_LOG_LEVEL=DEBUG` to see outbound HTTP requests.

## Data directories

```
data/
  raw/<dataset-name>/   # files downloaded by `sixsight download`
  prep/<dataset-name>/  # aggregated outputs written by CLI commands (e.g. monthly.csv)
  meta/<dataset-name>/  # hand-maintained reference files (e.g. codes_categories.csv)
```

## Web (`web/`)

A Vite + React static site that visualises prepared data from `data/prep/`.

```
web/
  public/data/     # CSV files consumed at runtime (copy from data/prep/ before dev/build)
  src/
    components/    # one file per page section; add new sections here
    hooks/         # data-loading hooks (useCSV)
  index.css        # design tokens (CSS custom properties) and global styles
```

```bash
cd web
npm install        # first time
npm run dev        # dev server at http://localhost:5173
npm run build      # production build → web/dist/
```

## Dependencies
Uses [CKAN API](https://docs.ckan.org/en/latest/api/index.html) to access the data

## Commit Message Convention

This project follows **Conventional Commits** (https://www.conventionalcommits.org).
All commits generated or suggested by Claude must conform to this spec.

### Format
<type>[optional scope]: <description>
[optional body]
[optional footer(s)]

### Allowed types

- feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

### Scopes for this project (pick the closest match)

- web, python, research

### Rules

1. Subject line ≤ 72 characters, lowercase, no trailing period.
2. Use imperative mood: "add feature" not "added feature".
3. Breaking changes: append `!` to the type OR add a `BREAKING CHANGE:` footer.
4Never squash unrelated changes into one commit — split them.

## Key conventions and guidelines

- Dependency injection: `TorontoOpenDataClient(config=SETTINGS)` — always pass config explicitly, never use the global inside library code.
- Raw JSON from the API is typed `dict[str, Any]`; use `object` only when values won't be accessed.
- mypy is strict. All functions including tests need return type annotations.
- Git hooks (pre-commit) run ruff (fix + format) and mypy on every commit.
- CLI lazy imports: in `cli/app.py`, `sixsight.*` imports must be inside the command function body, not at module level. `typer`, `rich`, and stdlib belong at the top of the file. This keeps `--help` fast and isolates heavy deps per command.
- **After every significant change** — new CLI command, new data pipeline, new web section, new dependency, changed directory layout — update `CLAUDE.md` (architecture / conventions), `README.md` (user-facing instructions), and `CONTRIBUTING.md` (dev setup / release process). Keep them in sync with the actual codebase.
