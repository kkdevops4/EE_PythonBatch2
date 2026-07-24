"""
generate_dataset.py
-------------------
Generates a realistic one-day EV Battery Management System dataset.
Saves the Excel file to  data/sample_bms_data.xlsx

main.py calls this automatically if the file is missing,
so users never need to run it separately.
"""

import numpy as np
import pandas as pd
from pathlib import Path


def _build_mode_schedule():
    """
    Build a realistic minute-by-minute operating-mode plan for one day.
    Each entry is (mode, number_of_rows).  One row = 50 seconds.
    72 rows = 1 hour.
    """
    return [
        # ── Night / early morning — vehicle parked ──
        ("Parking",   72),   # 00:00 – 01:00
        ("Parking",   72),   # 01:00 – 02:00
        ("Parking",   72),   # 02:00 – 03:00
        ("Parking",   72),   # 03:00 – 04:00
        ("Parking",   72),   # 04:00 – 05:00
        ("Parking",   72),   # 05:00 – 06:00
        ("Parking",   36),   # 06:00 – 06:30

        # ── Morning commute ──
        ("Driving",   54),   # 06:30 – 07:15
        ("Parking",   27),   # 07:15 – 07:37  quick stop
        ("Driving",   36),   # 07:37 – 08:07

        # ── Parked at work ──
        ("Parking",  108),   # 08:07 – 09:37

        # ── Mid-morning errands ──
        ("Driving",   36),   # 09:37 – 10:07
        ("Parking",   54),   # 10:07 – 10:52
        ("Driving",   27),   # 10:52 – 11:15
        ("Parking",   54),   # 11:15 – 12:00

        # ── Lunch drive ──
        ("Driving",   36),   # 12:00 – 12:30
        ("Parking",   36),   # 12:30 – 13:00
        ("Driving",   27),   # 13:00 – 13:22
        ("Parking",   72),   # 13:22 – 14:22

        # ── Afternoon drive + first charge ──
        ("Driving",   54),   # 14:22 – 15:07
        ("Charging",  90),   # 15:07 – 16:22  charging session 1
        ("Parking",   36),   # 16:22 – 16:52

        # ── Evening commute ──
        ("Driving",   54),   # 16:52 – 17:37
        ("Parking",   36),   # 17:37 – 18:07
        ("Driving",   36),   # 18:07 – 18:37

        # ── Home charging ──
        ("Charging",  72),   # 18:37 – 19:37  charging session 2
        ("Parking",   36),   # 19:37 – 20:07

        # ── Short evening trip ──
        ("Driving",   27),   # 20:07 – 20:30

        # ── Night parking ──
        ("Parking",   72),   # 20:30 – 21:30
        ("Parking",   72),   # 21:30 – 22:30
        ("Parking",   72),   # 22:30 – 23:30
        ("Parking",   37),   # 23:30 – 23:59:10
    ]


def generate_bms_dataset(output_path="data/sample_bms_data.xlsx"):
    """Generate a full-day BMS dataset and save it as an Excel file."""
    np.random.seed(42)

    # Flatten schedule into per-row mode list
    modes = []
    for mode, count in _build_mode_schedule():
        modes.extend([mode] * count)

    total_rows = len(modes)

    # Timestamps every 50 seconds starting 2026-07-21 00:00:00
    start = pd.Timestamp("2026-07-21 00:00:00")
    timestamps = [start + pd.Timedelta(seconds=50 * i) for i in range(total_rows)]

    # Pre-allocate arrays
    soc         = np.zeros(total_rows)
    soh         = np.zeros(total_rows)
    voltage     = np.zeros(total_rows)
    current     = np.zeros(total_rows)
    temperature = np.zeros(total_rows)
    speed       = np.zeros(total_rows)
    power       = np.zeros(total_rows)
    charging_status = []

    # Starting state
    cur_soc     = 85.0
    cur_temp    = 28.0
    cur_voltage = 370.0

    for i in range(total_rows):
        mode = modes[i]

        if mode == "Driving":
            cur_soc -= np.random.uniform(0.02, 0.06)
            cur_soc = max(cur_soc, 10.0)
            cur_voltage = 320 + (cur_soc / 100) * 80 + np.random.normal(0, 0.5)
            cur_i = np.random.uniform(30, 150)
            cur_temp += np.random.uniform(0.01, 0.04)
            cur_temp = min(cur_temp, 50.0)
            spd = np.random.uniform(15, 80)
            charging_status.append("No")

        elif mode == "Charging":
            cur_soc += np.random.uniform(0.04, 0.10)
            cur_soc = min(cur_soc, 100.0)
            cur_voltage = 340 + (cur_soc / 100) * 60 + np.random.normal(0, 0.3)
            cur_i = -np.random.uniform(20, 120)
            cur_temp += np.random.uniform(0.005, 0.025)
            cur_temp = min(cur_temp, 45.0)
            spd = 0.0
            charging_status.append("Yes")

        else:  # Parking
            cur_soc -= np.random.uniform(0.0, 0.003)
            cur_soc = max(cur_soc, 10.0)
            cur_voltage = 330 + (cur_soc / 100) * 70 + np.random.normal(0, 0.2)
            cur_i = np.random.normal(0, 0.3)
            cur_temp += (28.0 - cur_temp) * 0.005
            cur_temp += np.random.normal(0, 0.03)
            spd = 0.0
            charging_status.append("No")

        soc[i]         = round(cur_soc, 2)
        soh[i]         = round(96.5 + np.random.normal(0, 0.05), 2)
        voltage[i]     = round(cur_voltage, 1)
        current[i]     = round(cur_i, 1)
        temperature[i] = round(cur_temp, 1)
        speed[i]       = round(spd, 1)
        power[i]       = round(abs(cur_voltage * cur_i) / 1000, 2)

    df = pd.DataFrame({
        "Timestamp":       timestamps,
        "Vehicle_ID":      "EV001",
        "Mode":            modes,
        "SOC":             soc,
        "SOH":             soh,
        "Voltage":         voltage,
        "Current":         current,
        "Temperature":     temperature,
        "Speed":           speed,
        "Power":           power,
        "Charging_Status": charging_status,
    })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Dataset saved -> {output_path}  ({len(df)} rows)")
    return df


if __name__ == "__main__":
    generate_bms_dataset()
