from __future__ import annotations

import csv
from collections.abc import Iterable
from io import StringIO

import httpx

from pipeline.settings import settings


def fetch_csv_text(url: str) -> str:
    with httpx.Client(timeout=settings.timeout_seconds, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text


def parse_csv_rows(csv_text: str) -> Iterable[dict[str, str]]:
    reader = csv.DictReader(StringIO(csv_text))
    for row in reader:
        yield {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

