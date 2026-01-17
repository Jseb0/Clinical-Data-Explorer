from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict


class TrialOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    title: str
    condition: str | None = None
    sponsor: str | None = None
    sponsor_type: str | None = None
    start_date: date | None = None
    status: str | None = None


class TrialsPage(BaseModel):
    page: int
    limit: int
    total: int
    pages: int
    items: list[TrialOut]


class CountItem(BaseModel):
    name: str
    count: int


class TimeCountItem(BaseModel):
    period: str
    count: int


class SponsorTypeItem(BaseModel):
    sponsor_type: str
    count: int

