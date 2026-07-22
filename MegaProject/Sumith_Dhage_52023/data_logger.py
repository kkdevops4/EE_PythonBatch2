from datetime import datetime
from pathlib import Path
import pandas as pd
from config import LOG_FILE

SUMMARY_COLUMNS = [
    "Session ID", "Start Timestamp", "Stop Timestamp", "Duration (s)",
    "Stop Command Time (s)", "Stop Command Speed (km/h)", "Post-Stop Duration (s)",
    "Maximum Velocity (km/h)", "Average Velocity (km/h)",
    "Final Pre-Stop Velocity (km/h)", "Maximum Accelerator (%)",
    "Maximum Brake (%)", "Completion Status",
]
DETAIL_COLUMNS = [
    "Session ID", "Sample Number", "Elapsed Time (s)", "Accelerator (%)",
    "Brake (%)", "Mapped Output", "Driving Force (N)",
    "Aerodynamic Resistance (N)", "Rolling Resistance (N)",
    "Environmental Resistance (N)", "Brake Force (N)", "Net Force (N)",
    "Acceleration (m/s^2)", "Velocity (km/h)", "Operating State",
]

class ExcelDataLogger:
    def __init__(self, path=LOG_FILE):
        self.path = Path(path)
        self.create_workbook()

    def create_workbook(self):
        if self.path.exists():
            return
        with pd.ExcelWriter(self.path, engine="openpyxl") as writer:
            self.write_sheets(writer, pd.DataFrame(columns=SUMMARY_COLUMNS), pd.DataFrame(columns=DETAIL_COLUMNS))

    def write_sheets(self, writer, summary, details):
        summary.to_excel(writer, sheet_name="SessionSummary", index=False)
        details.to_excel(writer, sheet_name="TimeStepLog", index=False)

    def get_next_session_id(self):
        summary = pd.read_excel(self.path, sheet_name="SessionSummary", engine="openpyxl")
        if summary.empty:
            return 1
        ids = pd.to_numeric(summary["Session ID"], errors="coerce").dropna()
        return 1 if ids.empty else int(ids.max()) + 1

    def make_record(self, session_id, state, result, sample_number):
        return {
            "Session ID": session_id, "Sample Number": sample_number,
            "Elapsed Time (s)": state.elapsed_time_seconds,
            "Accelerator (%)": round(state.accelerator_percentage, 3),
            "Brake (%)": round(state.brake_percentage, 3),
            "Mapped Output": round(result.mapped_output, 6),
            "Driving Force (N)": round(result.driving_force_n, 3),
            "Aerodynamic Resistance (N)": round(result.aerodynamic_force_n, 3),
            "Rolling Resistance (N)": round(result.rolling_force_n, 3),
            "Environmental Resistance (N)": round(result.environmental_resistance_n, 3),
            "Brake Force (N)": round(result.brake_force_n, 3),
            "Net Force (N)": round(result.net_force_n, 3),
            "Acceleration (m/s^2)": round(result.acceleration_m_s2, 6),
            "Velocity (km/h)": round(result.speed_kmh, 6),
            "Operating State": state.operating_state,
        }

    def make_summary(self, session_id, session_start, state, stop_time, stop_speed, records):
        speeds = [row["Velocity (km/h)"] for row in records] or [0]
        accelerators = [row["Accelerator (%)"] for row in records] or [0]
        brakes = [row["Brake (%)"] for row in records] or [0]
        total, stop_time, stop_speed = state.elapsed_time_seconds, stop_time or 0, stop_speed or 0
        return {
            "Session ID": session_id,
            "Start Timestamp": session_start.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "Stop Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            "Duration (s)": round(total, 3),
            "Stop Command Time (s)": round(stop_time, 3),
            "Stop Command Speed (km/h)": round(stop_speed, 6),
            "Post-Stop Duration (s)": round(total - stop_time, 3),
            "Maximum Velocity (km/h)": round(max(speeds), 6),
            "Average Velocity (km/h)": round(sum(speeds) / len(speeds), 6),
            "Final Pre-Stop Velocity (km/h)": round(stop_speed, 6),
            "Maximum Accelerator (%)": round(max(accelerators), 3),
            "Maximum Brake (%)": round(max(brakes), 3),
            "Completion Status": "Completed",
        }

    def save_session(self, summary_record, detailed_records):
        old_summary = pd.read_excel(self.path, sheet_name="SessionSummary", engine="openpyxl")
        old_details = pd.read_excel(self.path, sheet_name="TimeStepLog", engine="openpyxl")
        summary = pd.concat([old_summary, pd.DataFrame([summary_record])], ignore_index=True).reindex(columns=SUMMARY_COLUMNS)
        details = pd.concat([old_details, pd.DataFrame(detailed_records)], ignore_index=True).reindex(columns=DETAIL_COLUMNS)
        temporary = self.path.with_name("vehicle_simulation_log_temporary.xlsx")
        with pd.ExcelWriter(temporary, engine="openpyxl") as writer:
            self.write_sheets(writer, summary, details)
        temporary.replace(self.path)
