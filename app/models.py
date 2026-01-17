from __future__ import annotations

from sqlalchemy import Column, Date, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Trial(Base):  # type: ignore[misc, valid-type]
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(String(128), unique=True, index=True, nullable=False)
    title = Column(Text, nullable=False)
    condition = Column(String(256), index=True, nullable=True)
    sponsor = Column(String(256), index=True, nullable=True)
    sponsor_type = Column(String(64), index=True, nullable=True)
    start_date = Column(Date, index=True, nullable=True)
    status = Column(String(64), index=True, nullable=True)

    __table_args__ = (
        Index("ix_trials_condition_start", "condition", "start_date"),
    )

