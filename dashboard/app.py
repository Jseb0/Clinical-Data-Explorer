from __future__ import annotations

import os
from datetime import date

import pandas as pd
import requests  # type: ignore[import-untyped]
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

st.set_page_config(page_title="Clinical Trials Explorer", layout="wide")

st.title("Clinical Trials Data Explorer")
st.caption("Dashboard powered by FastAPI + SQLite ingestion pipeline")

st.sidebar.header("Filters")

q = st.sidebar.text_input("Search title (q)", value="")
condition = st.sidebar.text_input("Condition contains", value="")
sponsor = st.sidebar.text_input("Sponsor contains", value="")
status = st.sidebar.text_input("Status contains", value="")

col1, col2 = st.sidebar.columns(2)
start_from = col1.date_input("Start from", value=None)
start_to = col2.date_input("Start to", value=None)

limit = st.sidebar.slider("Rows per page", min_value=5, max_value=100, value=20, step=5)
page = st.sidebar.number_input("Page", min_value=1, value=1, step=1)

sort_by = st.sidebar.selectbox("Sort by", ["start_date", "title", "sponsor", "status"], index=0)
sort_dir = st.sidebar.selectbox("Sort direction", ["desc", "asc"], index=0)

interval = st.sidebar.selectbox("Time interval", ["month", "year"], index=0)

st.sidebar.button("Refresh")


def api_get(path: str, params: dict | None = None):
    url = f"{API_BASE}{path}"
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def optional_str(value: str) -> str | None:
    return value if value else None


def optional_date(value: date | None) -> str | None:
    return value.isoformat() if isinstance(value, date) else None


params = {
    "q": optional_str(q),
    "condition": optional_str(condition),
    "sponsor": optional_str(sponsor),
    "status": optional_str(status),
    "start_from": optional_date(start_from),
    "start_to": optional_date(start_to),
    "page": page,
    "limit": limit,
    "sort_by": sort_by,
    "sort_dir": sort_dir,
}
params = {k: v for k, v in params.items() if v is not None}

left, right = st.columns([2, 1])

with st.spinner("Loading trials..."):
    trials_page = api_get("/trials", params=params)

items = trials_page["items"]
df_trials = pd.DataFrame(items)

with left:
    st.subheader("Trials")
    st.write(
        f"Showing page **{trials_page['page']}** of **{trials_page['pages']}** "
        f"(**{trials_page['total']}** total trials)"
    )
    st.dataframe(df_trials, use_container_width=True, hide_index=True)

with right:
    st.subheader("Quick Stats")
    st.metric("Total trials (filtered)", trials_page["total"])
    st.metric("Pages", trials_page["pages"])
    st.metric("Rows on this page", len(items))

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Top Conditions")
    with st.spinner("Loading top conditions..."):
        top_conditions = api_get("/analytics/top-conditions", params={"limit": 10})
    df_cond = pd.DataFrame(top_conditions).rename(columns={"name": "condition"})
    if not df_cond.empty:
        st.bar_chart(df_cond.set_index("condition")["count"])
    else:
        st.info("No condition data available.")

with c2:
    st.subheader("Top Sponsors")
    with st.spinner("Loading sponsor breakdown..."):
        top_sponsors = api_get("/analytics/sponsor-breakdown", params={"limit": 10})
    df_spon = pd.DataFrame(top_sponsors).rename(columns={"name": "sponsor"})
    if not df_spon.empty:
        st.bar_chart(df_spon.set_index("sponsor")["count"])
    else:
        st.info("No sponsor data available.")

st.divider()

st.subheader("Trials Over Time")
with st.spinner("Loading time series..."):
    series = api_get("/analytics/trials-over-time", params={"interval": interval})
df_time = pd.DataFrame(series)
if not df_time.empty:
    df_time = df_time.sort_values("period")
    st.line_chart(df_time.set_index("period")["count"])
else:
    st.info("No date data available for time series.")

