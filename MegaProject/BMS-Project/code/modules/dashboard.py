"""
dashboard.py
------------
Renders mode-specific charts using Plotly Express.
Each function draws a set of charts for one operating mode.
"""

import streamlit as st
import plotly.express as px
import pandas as pd


# ── Shared dark layout applied to every chart ──
LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=40, r=20, t=45, b=35),
    title_font_size=15,
)


def _line(df, x, y, title, color="#0EA5E9"):
    """Helper — create a single time-series line chart."""
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_traces(line_color=color)
    fig.update_layout(**LAYOUT)
    return fig


# ═══════════════════════════════════════════════════════════
#  CHART SETS — one function per mode
# ═══════════════════════════════════════════════════════════

def show_all_charts(df: pd.DataFrame):
    """Charts when 'All' is selected — overview of the full day."""
    c1, c2 = st.columns(2)
    c1.plotly_chart(_line(df, "Timestamp", "SOC", "SOC vs Time"),
                    use_container_width=True)
    c2.plotly_chart(_line(df, "Timestamp", "Temperature",
                          "Temperature vs Time", "#F59E0B"),
                    use_container_width=True)

    c3, c4 = st.columns(2)
    c3.plotly_chart(_line(df, "Timestamp", "Voltage",
                          "Voltage vs Time", "#8B5CF6"),
                    use_container_width=True)

    # Mode distribution pie chart
    counts = df["Mode"].value_counts().reset_index()
    counts.columns = ["Mode", "Count"]
    fig = px.pie(counts, names="Mode", values="Count",
                 title="Mode Distribution", hole=0.4)
    fig.update_layout(**LAYOUT)
    c4.plotly_chart(fig, use_container_width=True)


def show_driving_charts(df: pd.DataFrame):
    """Charts when 'Driving' is selected."""
    if df.empty:
        st.info("No driving data available.")
        return
    c1, c2 = st.columns(2)
    c1.plotly_chart(_line(df, "Timestamp", "SOC", "SOC vs Time"),
                    use_container_width=True)
    c2.plotly_chart(_line(df, "Timestamp", "Speed",
                          "Speed vs Time", "#22C55E"),
                    use_container_width=True)

    c3, c4 = st.columns(2)
    c3.plotly_chart(_line(df, "Timestamp", "Power",
                          "Power vs Time", "#EF4444"),
                    use_container_width=True)
    c4.plotly_chart(_line(df, "Timestamp", "Temperature",
                          "Temperature vs Time", "#F59E0B"),
                    use_container_width=True)


def show_charging_charts(df: pd.DataFrame):
    """Charts when 'Charging' is selected."""
    if df.empty:
        st.info("No charging data available.")
        return
    c1, c2 = st.columns(2)
    c1.plotly_chart(_line(df, "Timestamp", "SOC", "SOC vs Time"),
                    use_container_width=True)
    c2.plotly_chart(_line(df, "Timestamp", "Voltage",
                          "Voltage vs Time", "#8B5CF6"),
                    use_container_width=True)

    c3, c4 = st.columns(2)
    # Show absolute current for readability
    tmp = df.copy()
    tmp["Current_Abs"] = tmp["Current"].abs()
    c3.plotly_chart(_line(tmp, "Timestamp", "Current_Abs",
                          "Charging Current (A)", "#06B6D4"),
                    use_container_width=True)
    c4.plotly_chart(_line(df, "Timestamp", "Temperature",
                          "Temperature vs Time", "#F59E0B"),
                    use_container_width=True)


def show_parking_charts(df: pd.DataFrame):
    """Charts when 'Parking' is selected."""
    if df.empty:
        st.info("No parking data available.")
        return
    c1, c2 = st.columns(2)
    c1.plotly_chart(_line(df, "Timestamp", "Voltage",
                          "Voltage Stability", "#8B5CF6"),
                    use_container_width=True)
    c2.plotly_chart(_line(df, "Timestamp", "Temperature",
                          "Temperature Trend", "#F59E0B"),
                    use_container_width=True)

    st.plotly_chart(_line(df, "Timestamp", "SOC", "SOC Stability"),
                    use_container_width=True)
