![CI](../../actions/workflows/ci.yml/badge.svg)

# Clinical Data Explorer (ETL + API + Dashboard)

End-to-end Python project that ingests public clinical trials data, validates and stores it,
exposes a FastAPI API with filtering + pagination, and provides a Streamlit dashboard with
analytics.

![Dashboard](docs/diagrams/dashboard.png)

## Problem it solves
Public clinical trials data is available but not easy to query or explore. This project turns
raw registry data into a clean, reproducible pipeline + API + dashboard so users can:
- search trials by title/condition/sponsor/status
- filter by date range
- view trends over time and top conditions/sponsors

## Architecture

Data Source (CSV)  
↓  
Ingestion + Validation (Pydantic)  
↓  
SQLite (local dev)  
↓  
FastAPI (search/filter/pagination + analytics)  
↓  
Streamlit Dashboard (consumes the API)

## Features
- ETL ingestion with validation and bad-row handling
- SQLite-backed relational storage (swappable later)
- FastAPI endpoints:
  - `/trials` with filters, sorting, pagination
  - `/analytics/*` for top conditions, sponsor breakdown, and trends over time
- Streamlit dashboard with interactive filters and charts
- Tests with pytest

## Quickstart

### 1) Create venv + install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings httpx python-dotenv pytest ruff mypy streamlit pandas requests
```

### 2) Configure dataset

Create a `.env` file:
```
SOURCE_URL=https://clinicaltrials.gov/api/v2/studies?format=csv&pageSize=1000
```

### 3) Initialise DB + ingest
```bash
python -m app.init_db
python -m scripts.ingest
```

### 4) Run API
```bash
uvicorn app.main:app --reload
```

API docs:

http://127.0.0.1:8000/docs

### 5) Run dashboard
```bash
streamlit run dashboard/app.py
```

## Run with Docker Compose
```bash
docker compose up --build
```

API: http://127.0.0.1:8000/docs

Dashboard: http://127.0.0.1:8501

## Example API usage

List trials: `GET /trials?limit=20&page=1`

Search title: `GET /trials?q=cancer&limit=10`

Filter condition: `GET /trials?condition=diabetes`

Date range: `GET /trials?start_from=2020-01-01&start_to=2023-12-31`

Top conditions: `GET /analytics/top-conditions?limit=10`

Trials over time: `GET /analytics/trials-over-time?interval=month`



Add caching in Streamlit and analytics endpoints

Add richer sponsor classification (industry vs academic vs government)
