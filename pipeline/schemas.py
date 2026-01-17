from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class TrialIn(BaseModel):
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    condition: str | None = None
    sponsor: str | None = None
    sponsor_type: str | None = None
    start_date: date | None = None
    status: str | None = None

