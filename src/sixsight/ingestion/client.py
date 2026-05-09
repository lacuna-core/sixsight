from typing import Any

import httpx
from loguru import logger

from sixsight.config import Settings
from sixsight.models.dataset import Dataset, Resource


class TorontoOpenDataClient:
    """Client for the City of Toronto CKAN Open Data API."""

    def __init__(self, config: Settings) -> None:
        self._base = str(config.toronto_open_data_base_url).rstrip("/")
        self._http = httpx.Client(timeout=config.request_timeout)

    def __enter__(self) -> TorontoOpenDataClient:
        return self

    def __exit__(self, *_: object) -> None:
        self._http.close()

    def _get(self, path: str, params: dict[str, Any]) -> httpx.Response:
        req = self._http.build_request("GET", f"{self._base}{path}", params=params)
        logger.debug("GET {}", req.url)
        resp = self._http.send(req)
        resp.raise_for_status()
        return resp

    def search_datasets(self, query: str, *, limit: int = 10) -> list[Dataset]:
        resp = self._get("/api/3/action/package_search", {"q": query, "rows": limit})
        return [self._parse_dataset(r) for r in resp.json()["result"]["results"]]

    def get_dataset(self, name_or_id: str) -> Dataset:
        resp = self._get("/api/3/action/package_show", {"id": name_or_id})
        return self._parse_dataset(resp.json()["result"])

    def _parse_dataset(self, raw: dict[str, Any]) -> Dataset:
        resources = [
            Resource(
                id=r["id"],
                name=r.get("name", ""),
                format=r.get("format", ""),
                url=r.get("url", ""),
                last_modified=r.get("last_modified"),
                size=r.get("size"),
            )
            for r in raw.get("resources", [])
        ]
        tags = [t["name"] for t in raw.get("tags", [])]
        return Dataset(
            id=raw["id"],
            title=raw.get("title", ""),
            name=raw.get("name", ""),
            notes=raw.get("notes", ""),
            organization=raw.get("organization", {}).get("title", "")
            if raw.get("organization")
            else "",
            tags=tags,
            resources=resources,
            last_refreshed=raw.get("last_refreshed"),
        )
