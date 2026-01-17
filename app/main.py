# ruff: noqa: B008
from __future__ import annotations

from collections.abc import Generator
from datetime import date
from math import ceil
from typing import Literal

from fastapi import Depends, FastAPI, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Trial
from app.schemas import CountItem, SponsorTypeItem, TimeCountItem, TrialOut, TrialsPage

app = FastAPI(title="UK Clinical Trials Data Explorer")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/trials", response_model=TrialsPage)
def list_trials(  # noqa: B008
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Search in title (case-insensitive)"),
    condition: str | None = Query(default=None, description="Filter by condition (contains)"),
    sponsor: str | None = Query(default=None, description="Filter by sponsor (contains)"),
    status: str | None = Query(default=None, description="Filter by status (contains)"),
    start_from: date | None = Query(default=None, description="Start date >= start_from"),
    start_to: date | None = Query(default=None, description="Start date <= start_to"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=200),
    sort_by: Literal["start_date", "title", "sponsor", "status"] = Query(
        default="start_date"
    ),
    sort_dir: Literal["asc", "desc"] = Query(default="desc"),
):
    query = db.query(Trial)

    if q:
        query = query.filter(Trial.title.ilike(f"%{q}%"))
    if condition:
        query = query.filter(Trial.condition.ilike(f"%{condition}%"))
    if sponsor:
        query = query.filter(Trial.sponsor.ilike(f"%{sponsor}%"))
    if status:
        query = query.filter(Trial.status.ilike(f"%{status}%"))
    if start_from:
        query = query.filter(Trial.start_date >= start_from)
    if start_to:
        query = query.filter(Trial.start_date <= start_to)

    total = query.count()

    sort_col = getattr(Trial, sort_by)
    if sort_dir == "asc":
        query = query.order_by(sort_col.asc().nulls_last())
    else:
        query = query.order_by(sort_col.desc().nulls_last())

    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    pages = ceil(total / limit) if total else 1
    return TrialsPage(
        page=page,
        limit=limit,
        total=total,
        pages=pages,
        items=[TrialOut.model_validate(x) for x in items],
    )


@app.get("/analytics/top-conditions", response_model=list[CountItem])
def top_conditions(  # noqa: B008
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
):
    rows = (
        db.query(Trial.condition, func.count(Trial.id))
        .filter(Trial.condition.isnot(None))
        .filter(Trial.condition != "")
        .group_by(Trial.condition)
        .order_by(func.count(Trial.id).desc())
        .limit(limit)
        .all()
    )
    return [CountItem(name=r[0], count=int(r[1])) for r in rows]


@app.get("/analytics/trials-over-time", response_model=list[TimeCountItem])
def trials_over_time(  # noqa: B008
    db: Session = Depends(get_db),
    interval: Literal["month", "year"] = Query(default="month"),
):
    fmt = "%Y-%m" if interval == "month" else "%Y"
    period_expr = func.strftime(fmt, Trial.start_date)
    rows = (
        db.query(period_expr.label("period"), func.count(Trial.id))
        .filter(Trial.start_date.isnot(None))
        .group_by("period")
        .order_by("period")
        .all()
    )
    out = []
    for period, count in rows:
        if period is None:
            continue
        out.append(TimeCountItem(period=str(period), count=int(count)))
    return out


@app.get("/analytics/sponsor-breakdown", response_model=list[CountItem])
def sponsor_breakdown(  # noqa: B008
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
):
    rows = (
        db.query(Trial.sponsor, func.count(Trial.id))
        .filter(Trial.sponsor.isnot(None))
        .filter(Trial.sponsor != "")
        .group_by(Trial.sponsor)
        .order_by(func.count(Trial.id).desc())
        .limit(limit)
        .all()
    )
    return [CountItem(name=r[0], count=int(r[1])) for r in rows]


@app.get("/analytics/sponsor-types", response_model=list[SponsorTypeItem])
def sponsor_types(  # noqa: B008
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Trial.sponsor_type, func.count(Trial.id))
        .filter(Trial.sponsor_type.isnot(None))
        .filter(Trial.sponsor_type != "")
        .group_by(Trial.sponsor_type)
        .order_by(func.count(Trial.id).desc())
        .all()
    )
    return [SponsorTypeItem(sponsor_type=r[0], count=int(r[1])) for r in rows]

