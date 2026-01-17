from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pipeline.schemas import TrialIn


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    try:
        return date.fromisoformat(value[:10])
    except Exception:
        return None


def row_to_trial(row: dict[str, Any]) -> TrialIn:
    source_id = (
        row.get("NCT Number")
        or row.get("NCTId")
        or row.get("id")
        or row.get("trial_id")
        or row.get("nct_id")
        or row.get("source_id")
    )
    title = (
        row.get("Study Title")
        or row.get("BriefTitle")
        or row.get("title")
        or row.get("brief_title")
        or row.get("study_title")
    )
    condition = (
        row.get("Conditions")
        or row.get("Condition")
        or row.get("condition")
        or row.get("conditions")
    )
    sponsor = (
        row.get("Sponsor")
        or row.get("LeadSponsorName")
        or row.get("sponsor")
        or row.get("lead_sponsor")
        or row.get("org_name")
    )
    sponsor_type = row.get("sponsor_type") or row.get("funding_type")
    status = (
        row.get("Study Status")
        or row.get("OverallStatus")
        or row.get("status")
        or row.get("overall_status")
    )

    start_date_raw = (
        row.get("Start Date")
        or row.get("StartDate")
        or row.get("start_date")
        or row.get("study_start")
        or row.get("start_date_str")
    )
    start_date = None
    if isinstance(start_date_raw, str):
        start_date = parse_date(start_date_raw)

    return TrialIn(
        source_id=str(source_id),
        title=str(title),
        condition=condition,
        sponsor=sponsor,
        sponsor_type=sponsor_type,
        start_date=start_date,
        status=status,
    )

