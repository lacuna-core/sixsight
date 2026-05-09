# SixSight 🏙️

SixSight is an open-source analytics platform that ingests, transforms, and visualizes datasets published by the City of Toronto. The project aims to surface meaningful insights from civic data — spanning transit, infrastructure, public safety, permits, demographics, and more — to support researchers, journalists, policymakers, and curious Torontonians.

The name is a nod to The 6ix, Toronto's cultural identity rooted in its area codes (416 / 647), fused with insight — the project's core purpose.

Powered by the [City of Toronto Open Data Portal](https://open.toronto.ca/).

---

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager
- Python 3.14 (uv will install it automatically if missing)

### Install

```bash
git clone https://github.com/your-org/sixsight.git
cd sixsight
uv sync --dev
uv run pre-commit install
```

`uv sync` creates a `.venv`, installs all dependencies (including dev tools), and pins versions from `uv.lock`. `pre-commit install` wires up the git hooks — after that, `ruff check --fix` and `ruff format` run automatically on every commit.

To run commands:
```bash
uv run command -xyz
# or
source .venv/bin/activate
command -xyz
```

### Configuration

Copy the example env file and edit as needed:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `SIXSIGHT_LOG_LEVEL` | `INFO` | Logging verbosity |
| `SIXSIGHT_REQUEST_TIMEOUT` | `30.0` | HTTP timeout in seconds |
| `SIXSIGHT_CACHE_DIR` | `.cache` | Local cache directory |

All variables are optional — the defaults work out of the box.

### Run the test suite

```bash
pytest
```

Coverage report is printed automatically. To open an HTML report:

```bash
pytest --cov-report=html && open htmlcov/index.html
```

### Lint and type-check

```bash
ruff check          # lint
ruff check --fix    # fix linting errors
ruff format         # format
mypy                # type-check
```

---

## CLI usage

All commands are available via the `sixsight` entry point:

```bash
sixsight --help
# Install completion for the current shell
sixsight --install-completion
```

### Search datasets

Find datasets by keyword:

```bash
sixsight search "ttc delays"
sixsight search "bicycle" --limit 5
sixsight search "building permits"
```

```
                    Results for "ttc delays"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┓
┃ Name                        ┃ Title                   ┃ Formats ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━┩
│ ttc-subway-delay-data       │ TTC Subway Delay Data   │ XLSX    │
│ ttc-streetcar-delay-data    │ TTC Streetcar Delay Data│ XLSX    │
│ ttc-bus-delay-data          │ TTC Bus Delay Data      │ XLSX    │
└─────────────────────────────┴─────────────────────────┴─────────┘
```

### Inspect a dataset

Show metadata and available resources for a dataset by name or ID:

```bash
sixsight info ttc-subway-delay-data
sixsight info ttc-bus-delay-data
```

```
TTC Subway Delay Data
ID: 996cfe8d-fb35-4395-ae32-d7b64fe86694
Org: Toronto Transit Commission
Tags: transit, ttc, subway, delays

Records of delays on the TTC subway network, including date, time,
station, line, and minutes delayed.
```
