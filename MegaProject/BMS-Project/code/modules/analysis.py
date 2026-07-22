"""
analysis.py
-----------
Computes KPIs and builds the summary report data.
"""

import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    """
    Calculate the five KPI values displayed as metric cards.
    Returns a dict of  label -> rounded value.
    """
    return {
        "Avg SOC (%)":     round(df["SOC"].mean(), 1),
        "Avg SOH (%)":     round(df["SOH"].mean(), 1),
        "Avg Voltage (V)": round(df["Voltage"].mean(), 1),
        "Avg Temp (°C)":   round(df["Temperature"].mean(), 1),
        "Avg Power (kW)":  round(df["Power"].mean(), 2),
    }


def build_report_data(df: pd.DataFrame) -> list:
    """
    Create a list of (metric_name, value) tuples for the report.
    Used by both the dashboard table and the PDF generator.
    """
    return [
        ("Average SOC (%)",            round(df["SOC"].mean(), 2)),
        ("Average SOH (%)",            round(df["SOH"].mean(), 2)),
        ("Average Voltage (V)",        round(df["Voltage"].mean(), 2)),
        ("Average Temperature (°C)",   round(df["Temperature"].mean(), 2)),
        ("Maximum Temperature (°C)",   round(df["Temperature"].max(), 2)),
        ("Minimum SOC (%)",            round(df["SOC"].min(), 2)),
        ("Driving Records",            int((df["Mode"] == "Driving").sum())),
        ("Charging Records",           int((df["Mode"] == "Charging").sum())),
        ("Parking Records",            int((df["Mode"] == "Parking").sum())),
        ("Total Records",              len(df)),
        ("Driving Duration (min)",     round((df["Mode"] == "Driving").sum() * 50 / 60, 1)),
        ("Charging Duration (min)",    round((df["Mode"] == "Charging").sum() * 50 / 60, 1)),
        ("Parking Duration (min)",     round((df["Mode"] == "Parking").sum() * 50 / 60, 1)),
    ]


def report_as_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Convert report data into a two-column DataFrame for display."""
    data = build_report_data(df)
    return pd.DataFrame(data, columns=["Metric", "Value"])
