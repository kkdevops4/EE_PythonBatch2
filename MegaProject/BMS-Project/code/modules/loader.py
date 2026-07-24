"""
loader.py
---------
Loads and cleans the BMS Excel dataset.
All file I/O lives here so other modules stay pure.
"""

import pandas as pd
import streamlit as st


@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Read the BMS Excel file and return a clean DataFrame.
    Result is cached so repeated dashboard reruns are instant.
    """
    df = pd.read_excel(filepath, engine="openpyxl")

    # Ensure Timestamp is proper datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Sort chronologically
    df = df.sort_values("Timestamp").reset_index(drop=True)

    return df


def filter_by_mode(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """
    Return only rows matching the selected mode.
    If mode is 'All', return the full dataset unchanged.
    """
    if mode == "All":
        return df
    return df[df["Mode"] == mode].reset_index(drop=True)
