# Contributing to SixSight

Thanks for your interest in contributing. This document covers dev environment setup, testing, project conventions, and how to cut a release.

For user-facing documentation — installation, CLI usage, and the web interface — see [README.md](README.md).

---

## Dev environment setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- [gh](https://github.com/cli/cli) — GitHub CLI (required to create releases)
- [git-cliff](https://git-cliff.org/docs/) — changelog generator (required to cut a release)
- [Node.js](https://nodejs.org/) 24+ (required only for web development)

### Install

```bash
git clone https://github.com/lacuna-core/sixsight.git
cd sixsight
uv sync --dev
uv run pre-commit install
```

`uv sync --dev` creates `.venv` and installs all dependencies including dev tools (pytest, ruff, mypy, pre-commit), pinned from `uv.lock`.

`pre-commit install` wires up the git hooks — after that, `ruff check --fix`, `ruff format`, and `mypy` run automatically on every commit.

---

## Running the test suite

```bash
uv run pytest
```

Coverage is printed automatically. To open an HTML report:

```bash
uv run pytest --cov-report=html && open htmlcov/index.html
```

---

## Lint and type-check

```bash
uv run ruff check          # lint
uv run ruff check --fix    # fix linting errors automatically
uv run ruff format         # format
uv run mypy                # type-check (strict mode)
```

All three run in CI and via the pre-commit hooks.

---

## Architecture overview

`src/sixsight/` follows a layered structure:

- **`config.py`** — `Settings` (pydantic-settings, `SIXSIGHT_` prefix). The singleton `SETTINGS` is passed explicitly to clients; library code never reads it directly.
- **`ingestion/client.py`** — `TorontoOpenDataClient` handles all HTTP via the CKAN API.
- **`models/dataset.py`** — Pydantic v2 models (`Dataset`, `Resource`) for API responses.
- **`transforms/pipeline.py`** — composable `Pipeline` of `Transform` callables operating on `polars.DataFrame`.
- **`viz/charts.py`** — thin wrappers over `great_tables` for tabular output.
- **`cli/app.py`** — Typer CLI. Sub-command groups (e.g. `cli/ttc_subway_delay.py`) register via `app.add_typer(...)`.

For deeper conventions — dependency injection patterns, mypy strict requirements, CLI lazy import rules — see [CLAUDE.md](CLAUDE.md).

---

## Web interface (local development)

The `web/` directory contains a Vite + React static site that visualises data from `data/prep/`.

### First-time setup

```bash
# Generate the prepared data the site consumes
ss subway aggregate
cp data/prep/ttc-subway-delay-data/monthly.csv web/public/data/monthly.csv

cd web
npm install
```

### Dev server

```bash
cd web
npm run dev
```

The site is available at http://localhost:5173.

### Production build

```bash
cd web
npm run build      # output → web/dist/
npm run preview    # serve the build locally to verify
```

---

## Commit conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org). The commit-msg hook enforces the format on every commit.

```
<type>[optional scope]: <description>
```

**Allowed types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Scopes:** `web`, `python`, `research`

Rules: subject ≤ 72 characters, lowercase, no trailing period, imperative mood ("add feature" not "added feature"). Breaking changes: append `!` to the type or add a `BREAKING CHANGE:` footer.

---

## Cutting a release

```bash
# 1. Bump the version in pyproject.toml, then commit
git commit -m "chore: bump version to 0.2.0"

# 2. Tag and push
git tag v0.2.0
git push origin main
git push origin v0.2.0
```

GitHub Actions will create a draft release with auto-generated notes. Review and publish it on [GitHub Releases](https://github.com/lacuna-core/sixsight/releases).

To preview release notes locally:

```bash
git cliff --latest --strip header
```
