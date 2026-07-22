"""
main.py
-------
EV Battery Management System (BMS) Data Analysis Dashboard.

Launch with:
    streamlit run main.py

Everything loads automatically — no extra steps needed.
"""

import os
import streamlit as st

# ── Page config (must be the very first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="EV BMS Dashboard",
    page_icon="🔋",
    layout="wide",
)

from modules.loader import load_data, filter_by_mode
from modules.analysis import compute_kpis, report_as_dataframe
from modules.report_pdf import generate_pdf_report
from modules.dashboard import (
    show_all_charts,
    show_driving_charts,
    show_charging_charts,
    show_parking_charts,
)

DATA_PATH = "data/sample_bms_data.xlsx"


# ── Auto-generate dataset if it doesn't exist ──────────────────────────────
if not os.path.exists(DATA_PATH):
    from generate_dataset import generate_bms_dataset
    generate_bms_dataset(DATA_PATH)


# ── Load data ───────────────────────────────────────────────────────────────
df = load_data(DATA_PATH)


# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.title("🔋 EV BMS Dashboard")
st.sidebar.markdown("---")

mode = st.sidebar.selectbox(
    "Select Mode",
    ["All", "Driving", "Charging", "Parking"],
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Vehicle: {df['Vehicle_ID'].iloc[0]}")
st.sidebar.caption(f"Date: {df['Timestamp'].dt.date.iloc[0]}")
st.sidebar.caption(f"Total records: {len(df):,}")


# ── Filter data by selected mode ───────────────────────────────────────────
filtered = filter_by_mode(df, mode)

if filtered.empty:
    st.warning(f"No data available for mode: {mode}")
    st.stop()


# ── Page title ──────────────────────────────────────────────────────────────
st.title("EV Battery Management System Dashboard")
st.caption(f"Mode: **{mode}**  ·  {len(filtered):,} records")


# ── KPI metric cards ───────────────────────────────────────────────────────
kpis = compute_kpis(filtered)
cols = st.columns(len(kpis))
for col, (label, value) in zip(cols, kpis.items()):
    col.metric(label, value)

st.markdown("---")


# ── Mode-specific charts ───────────────────────────────────────────────────
if mode == "All":
    show_all_charts(filtered)
elif mode == "Driving":
    show_driving_charts(filtered)
elif mode == "Charging":
    show_charging_charts(filtered)
else:
    show_parking_charts(filtered)


# ── Report section ─────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📊 Analysis Report")

# Show the report table
report_df = report_as_dataframe(df)
st.dataframe(report_df, use_container_width=True, hide_index=True)

# Generate PDF and offer download
pdf_bytes = generate_pdf_report(df)

st.download_button(
    "📄  Download Detailed Report (PDF)",
    data=pdf_bytes,
    file_name="EV_BMS_Analysis_Report.pdf",
    mime="application/pdf",
)
