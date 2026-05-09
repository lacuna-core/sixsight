from datetime import datetime

from pydantic import BaseModel, Field


class Resource(BaseModel):
    id: str
    name: str
    format: str
    url: str
    last_modified: datetime | None = None
    size: int | None = None


class Dataset(BaseModel):
    id: str
    title: str
    name: str
    notes: str = ""
    organization: str = ""
    tags: list[str] = Field(default_factory=list)
    resources: list[Resource] = Field(default_factory=list)
    last_refreshed: datetime | None = None
