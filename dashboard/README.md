## Dashboard

Run API:
```bash
uvicorn app.main:app --reload
```

Run dashboard:
```bash
streamlit run dashboard/app.py
```

Optional: point the dashboard to a deployed API:
```bash
API_BASE=https://your-api.example.com streamlit run dashboard/app.py
```

