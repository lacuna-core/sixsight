# SixSight 🏙️

SixSight is an open-source analytics platform that ingests, transforms, and visualises datasets published by the City of Toronto. The project aims to surface meaningful insights from civic data — spanning transit, infrastructure, public safety, permits, demographics, and more — to support researchers, journalists, policymakers, and curious Torontonians.

The name is a nod to The 6ix, Toronto's cultural identity rooted in its area codes (416 / 647), fused with insight — the project's core purpose.

Powered by the [City of Toronto Open Data Portal](https://open.toronto.ca/) via the [CKAN API](https://docs.ckan.org/en/latest/api/index.html).

---

## Getting started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — Python package manager

### Install

```bash
git clone https://github.com/lacuna-core/sixsight.git
cd sixsight
uv sync
```

To run commands:

```bash
uv run sixsight --help
# or activate the virtualenv
source .venv/bin/activate
sixsight --help
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

All variables are optional — the defaults work out of the box.

For dev environment setup, testing, linting, and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## CLI usage

All commands are available via the `sixsight` entry point:

```bash
sixsight --help
# Install shell completion
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
sixsight info ttc-bus-delay-data
sixsight info ttc-subway-delay-data -l
```

```
TTC Subway Delay Data
ID: 996cfe8d-fb35-4395-ae32-d7b64fe86694
Org: Toronto Transit Commission
Tags: transit, ttc, subway, delays

Records of delays on the TTC subway network, including date, time,
station, line, and minutes delayed.
```

### Download a dataset

Download all resource files for a dataset into `data/raw/<dataset-name>/`:

```bash
sixsight download ttc-subway-delay-data -f csv
```

Each resource file is saved alongside a `metadata.json` file containing the full dataset metadata.

### Data directories

```
data/
  raw/<dataset-name>/   # files downloaded by `sixsight download`
  prep/<dataset-name>/  # aggregated outputs written by CLI commands (e.g. monthly.csv)
  meta/<dataset-name>/  # hand-maintained reference files (e.g. codes_categories.csv)
```

### Subway delay analysis

Aggregate all TTC subway delay files into a monthly summary CSV:

```bash
sixsight subway aggregate
```

Output is written to `data/prep/ttc-subway-delay-data/monthly.csv`.

---

## Releases

Published releases and their changelogs are available on [GitHub Releases](https://github.com/lacuna-core/sixsight/releases).
