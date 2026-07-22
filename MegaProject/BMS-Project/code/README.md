# EV Battery Management System — Data Analysis Dashboard

A simple, beginner-friendly Python dashboard that analyzes one day of Electric Vehicle battery telemetry data with a downloadable PDF report.

## Folder Structure

```
EV-BMS-Analytics/
│
├── data/                        ← raw dataset (auto-generated)
│   └── sample_bms_data.xlsx
│
├── docs/                        ← study documents
│   ├── Dashboard_Study_Guide.pdf
│   └── Code_Explanation.pdf
│
├── modules/                     ← Python source modules
│   ├── loader.py                ← reads and cleans the Excel file
│   ├── analysis.py              ← KPI calculation and report data
│   ├── dashboard.py             ← Plotly charts for each mode
│   └── report_pdf.py            ← PDF report generator
│
├── output_data/                 ← generated PDF reports
├── processed_data/              ← cleaned / transformed data
│
├── generate_dataset.py          ← creates the sample dataset
├── main.py                      ← Streamlit entry point
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/your-username/EV-BMS-Analytics.git
cd EV-BMS-Analytics
pip install -r requirements.txt
```

## Run

```bash
streamlit run main.py
```

## Dashboard Features

- Sidebar mode selector — All, Driving, Charging, Parking
- KPI cards — Average SOC, SOH, Voltage, Temperature, Power
- Mode-specific Plotly charts
- Detailed PDF report with download button

## Dataset

11 columns, ~1,729 rows, 50-second intervals, one full day for vehicle EV001.
