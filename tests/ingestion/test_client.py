from typing import Any

from sixsight.config import Settings
from sixsight.ingestion.client import TorontoOpenDataClient
from sixsight.models.dataset import Dataset


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
