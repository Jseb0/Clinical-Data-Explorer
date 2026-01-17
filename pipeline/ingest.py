from __future__ import annotations

import logging
from collections.abc import Iterable

from pydantic import ValidationError

from app.db import SessionLocal
from app.models import Trial
from pipeline.fetch_csv import fetch_csv_text, parse_csv_rows
from pipeline.schemas import TrialIn
from pipeline.settings import settings
from pipeline.transform import row_to_trial

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def upsert_trials(trials: Iterable[TrialIn]) -> tuple[int, int]:
    db = SessionLocal()
    inserted = 0
    updated = 0
    try:
        for t in trials:
            existing = db.query(Trial).filter(Trial.source_id == t.source_id).first()
            if existing:
                existing.title = t.title  # type: ignore[assignment]
                existing.condition = t.condition  # type: ignore[assignment]
                existing.sponsor = t.sponsor  # type: ignore[assignment]
                existing.sponsor_type = t.sponsor_type  # type: ignore[assignment]
                existing.start_date = t.start_date  # type: ignore[assignment]
                existing.status = t.status  # type: ignore[assignment]
                updated += 1
            else:
                db.add(Trial(**t.model_dump()))
                inserted += 1
        db.commit()
    finally:
        db.close()
    return inserted, updated


def ingest_from_url(url: str) -> dict:
    csv_text = fetch_csv_text(url)
    trials: list[TrialIn] = []
    bad_rows = 0

    for row in parse_csv_rows(csv_text):
        try:
            trial = row_to_trial(row)
            trials.append(trial)
        except (ValidationError, TypeError, ValueError):
            bad_rows += 1

    inserted, updated = upsert_trials(trials)
    return {
        "inserted": inserted,
        "updated": updated,
        "bad_rows": bad_rows,
        "total_parsed": len(trials) + bad_rows,
    }


def main() -> None:
    if not settings.source_url:
        raise SystemExit("SOURCE_URL is empty. Put a dataset URL in .env")
    result = ingest_from_url(settings.source_url)
    logger.info("Ingestion complete: %s", result)


if __name__ == "__main__":
    main()

