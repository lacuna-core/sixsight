from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from sixsight.cli.app import app
from sixsight.models.dataset import Dataset, Resource

runner = CliRunner()

_DT = datetime(2024, 6, 1, tzinfo=UTC)


@pytest.fixture
def sample_dataset() -> Dataset:
    return Dataset(
        id="abc-123",
        name="ttc-subway-delay-data",
        title="TTC Subway Delays",
        notes="Delay records.",
        organization="TTC",
        tags=["transit"],
        resources=[
            Resource(
                id="r1",
                name="2024 CSV",
                format="CSV",
                url="https://example.com/data.csv",
                last_modified=_DT,
            ),
            Resource(
                id="r2",
                name="2024 JSON",
                format="JSON",
                url="https://example.com/data.json",
                last_modified=_DT,
            ),
        ],
    )


def _mock_client(dataset: Dataset) -> MagicMock:
    mock = MagicMock()
    mock.__enter__.return_value = mock
    mock.get_dataset.return_value = dataset
    return mock


def test_download_fetches_all_resources(sample_dataset: Dataset, tmp_path: Path) -> None:
    with patch(
        "sixsight.ingestion.client.TorontoOpenDataClient", return_value=_mock_client(sample_dataset)
    ):
        result = runner.invoke(
            app, ["download", "ttc-subway-delay-data", "--data-dir", str(tmp_path)]
        )

    assert result.exit_code == 0, result.output
    dataset_dir = tmp_path / "ttc-subway-delay-data"
    assert (dataset_dir / "data.csv.json").exists()
    assert (dataset_dir / "data.json.json").exists()


def test_download_format_filter(sample_dataset: Dataset, tmp_path: Path) -> None:
    mock = _mock_client(sample_dataset)
    with patch("sixsight.ingestion.client.TorontoOpenDataClient", return_value=mock):
        result = runner.invoke(
            app,
            ["download", "ttc-subway-delay-data", "--format", "CSV", "--data-dir", str(tmp_path)],
        )

    assert result.exit_code == 0, result.output
    assert mock.download_resource.call_count == 1
    downloaded_resource: Resource = mock.download_resource.call_args[0][0]
    assert downloaded_resource.format == "CSV"


def test_download_format_filter_case_insensitive(sample_dataset: Dataset, tmp_path: Path) -> None:
    mock = _mock_client(sample_dataset)
    with patch("sixsight.ingestion.client.TorontoOpenDataClient", return_value=mock):
        result = runner.invoke(
            app,
            ["download", "ttc-subway-delay-data", "--format", "csv", "--data-dir", str(tmp_path)],
        )

    assert result.exit_code == 0, result.output
    assert mock.download_resource.call_count == 1


def test_download_skips_unchanged_resources(sample_dataset: Dataset, tmp_path: Path) -> None:
    import json

    dataset_dir = tmp_path / "ttc-subway-delay-data"
    dataset_dir.mkdir()
    for resource, filename in zip(sample_dataset.resources, ["data.csv", "data.json"], strict=True):
        (dataset_dir / f"{filename}.json").write_text(json.dumps(resource.model_dump(mode="json")))

    mock = _mock_client(sample_dataset)
    with patch("sixsight.ingestion.client.TorontoOpenDataClient", return_value=mock):
        result = runner.invoke(
            app, ["download", "ttc-subway-delay-data", "--data-dir", str(tmp_path)]
        )

    assert result.exit_code == 0, result.output
    mock.download_resource.assert_not_called()
    assert "2 skipped" in result.output


def test_download_refetches_when_last_modified_changed(
    sample_dataset: Dataset, tmp_path: Path
) -> None:
    import json

    older_resources = [
        Resource(
            id="r1",
            name="2024 CSV",
            format="CSV",
            url="https://example.com/data.csv",
            last_modified=datetime(2024, 1, 1, tzinfo=UTC),
        ),
        Resource(
            id="r2",
            name="2024 JSON",
            format="JSON",
            url="https://example.com/data.json",
            last_modified=datetime(2024, 1, 1, tzinfo=UTC),
        ),
    ]
    dataset_dir = tmp_path / "ttc-subway-delay-data"
    dataset_dir.mkdir()
    for resource, filename in zip(older_resources, ["data.csv", "data.json"], strict=True):
        (dataset_dir / f"{filename}.json").write_text(json.dumps(resource.model_dump(mode="json")))

    mock = _mock_client(sample_dataset)
    with patch("sixsight.ingestion.client.TorontoOpenDataClient", return_value=mock):
        result = runner.invoke(
            app, ["download", "ttc-subway-delay-data", "--data-dir", str(tmp_path)]
        )

    assert result.exit_code == 0, result.output
    assert mock.download_resource.call_count == 2


def test_download_metadata_written(sample_dataset: Dataset, tmp_path: Path) -> None:
    with patch(
        "sixsight.ingestion.client.TorontoOpenDataClient", return_value=_mock_client(sample_dataset)
    ):
        runner.invoke(app, ["download", "ttc-subway-delay-data", "--data-dir", str(tmp_path)])

    dataset_dir = tmp_path / "ttc-subway-delay-data"
    for resource, filename in zip(sample_dataset.resources, ["data.csv", "data.json"], strict=True):
        loaded = Resource.model_validate_json((dataset_dir / f"{filename}.json").read_text())
        assert loaded.id == resource.id
        assert loaded.last_modified == resource.last_modified
