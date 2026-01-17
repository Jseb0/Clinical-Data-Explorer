FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip && \
    pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings httpx python-dotenv && \
    pip install pytest ruff mypy streamlit pandas requests

EXPOSE 8000 8501

