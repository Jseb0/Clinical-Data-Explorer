import os

import requests  # type: ignore[import-untyped]

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

r = requests.get(f"{API_BASE}/health", timeout=10)
r.raise_for_status()
print("OK:", r.json())

