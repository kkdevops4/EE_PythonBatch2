from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "vehicle_simulation_log.xlsx"
PHYSICS_STEP_SECONDS, PHYSICS_TIMER_MS = 0.005, 5
TELEMETRY_REFRESH_MS, GRAPH_REFRESH_MS = 50, 100
VEHICLE_MASS_KG, AIR_DENSITY_KG_M3 = 1350.0, 1.225
DRAG_COEFFICIENT, FRONTAL_AREA_M2 = 0.30, 2.20
ROLLING_RESISTANCE_COEFFICIENT, GRAVITY_M_S2 = 0.012, 9.81
MAXIMUM_DRIVE_FORCE_N, MAXIMUM_BRAKE_FORCE_N = 4200.0, 7000.0
MAXIMUM_SPEED_KMH, STATIONARY_SPEED_KMH = 160.0, 0.05
ACCELERATOR_RISE_RATE, ACCELERATOR_RELEASE_RATE = 35.0, 45.0
BRAKE_RISE_RATE, BRAKE_RELEASE_RATE = 55.0, 70.0
SPEED_BREAKPOINTS = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 120, 140, 160], dtype=float)
PEDAL_BREAKPOINTS = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], dtype=float)

def create_default_drive_map():
    values = np.zeros((len(SPEED_BREAKPOINTS), len(PEDAL_BREAKPOINTS)))
    for row, speed in enumerate(SPEED_BREAKPOINTS):
        for column, pedal in enumerate(PEDAL_BREAKPOINTS):
            values[row, column] = pedal / 100 * max(0.30, 1 - 0.0042 * speed)
    return np.maximum(values, 0.0)

DRIVE_MAP = create_default_drive_map()
