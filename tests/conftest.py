from typing import Any

import pytest


@pytest.fixture
def sample_dataset_payload() -> dict[str, Any]:
    return {
        "id": "abc-123",
        "title": "TTC Subway Delays",
        "name": "ttc-subway-delay-data",
        "notes": "Delay records for TTC subway lines.",
        "organization": {"title": "Toronto Transit Commission"},
        "tags": [{"name": "transit"}, {"name": "ttc"}],
        "resources": [
            {
                "id": "r1",
                "name": "2024 data",
                "format": "CSV",
                "url": "https://example.com/data.csv",
            }
        ],
    }
