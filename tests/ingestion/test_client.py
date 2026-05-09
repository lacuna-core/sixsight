from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from sixsight.config import Settings
from sixsight.ingestion.client import TorontoOpenDataClient
from sixsight.models.dataset import Dataset, Resource


def test_parse_dataset(sample_dataset_payload: dict[str, Any]) -> None:
    client = TorontoOpenDataClient(config=Settings())
    ds = client._parse_dataset(sample_dataset_payload)

    assert isinstance(ds, Dataset)
    assert ds.id == "abc-123"
    assert ds.name == "ttc-subway-delay-data"
    assert ds.organization == "Toronto Transit Commission"
    assert "transit" in ds.tags
    assert len(ds.resources) == 1
    assert ds.resources[0].format == "CSV"


def test_download_resource_writes_file(tmp_path: Path) -> None:
    resource = Resource(id="r1", name="data", format="CSV", url="https://example.com/data.csv")
    dest = tmp_path / "data.csv"

    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.iter_bytes.return_value = [b"col1,col2\n", b"1,2\n"]

    client = TorontoOpenDataClient(config=Settings())
    with patch.object(client._http, "stream", return_value=mock_resp):
        client.download_resource(resource, dest)

    assert dest.read_bytes() == b"col1,col2\n1,2\n"


def test_download_resource_creates_parent_dirs(tmp_path: Path) -> None:
    resource = Resource(id="r1", name="data", format="CSV", url="https://example.com/data.csv")
    dest = tmp_path / "nested" / "dir" / "data.csv"

    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    mock_resp.raise_for_status = MagicMock()
    mock_resp.iter_bytes.return_value = [b""]

    client = TorontoOpenDataClient(config=Settings())
    with patch.object(client._http, "stream", return_value=mock_resp):
        client.download_resource(resource, dest)

    assert dest.exists()
