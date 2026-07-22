from dataclasses import dataclass
import numpy as np
from config import (
    ACCELERATOR_RELEASE_RATE, ACCELERATOR_RISE_RATE, AIR_DENSITY_KG_M3,
    BRAKE_RELEASE_RATE, BRAKE_RISE_RATE, DRAG_COEFFICIENT, DRIVE_MAP,
    FRONTAL_AREA_M2, GRAVITY_M_S2, MAXIMUM_BRAKE_FORCE_N,
    MAXIMUM_DRIVE_FORCE_N, MAXIMUM_SPEED_KMH, PEDAL_BREAKPOINTS,
    ROLLING_RESISTANCE_COEFFICIENT, SPEED_BREAKPOINTS, STATIONARY_SPEED_KMH,
    VEHICLE_MASS_KG,
)

@dataclass
class VehicleState:
    accelerator_percentage: float = 0.0
    brake_percentage: float = 0.0
    vehicle_speed_kmh: float = 0.0
    vehicle_acceleration_m_s2: float = 0.0
    elapsed_time_seconds: float = 0.0
    operating_state: str = "STOPPED"

@dataclass(frozen=True)
class PhysicsResult:
    mapped_output: float
    driving_force_n: float
    aerodynamic_force_n: float
    rolling_force_n: float
    environmental_resistance_n: float
    brake_force_n: float
    net_force_n: float
    acceleration_m_s2: float
    speed_kmh: float

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def lookup_drive_demand(speed, pedal):
    speed = clamp(speed, SPEED_BREAKPOINTS[0], SPEED_BREAKPOINTS[-1])
    pedal = clamp(pedal, PEDAL_BREAKPOINTS[0], PEDAL_BREAKPOINTS[-1])
    values = [np.interp(speed, SPEED_BREAKPOINTS, DRIVE_MAP[:, column]) for column in range(len(PEDAL_BREAKPOINTS))]
    return max(0.0, float(np.interp(pedal, PEDAL_BREAKPOINTS, values)))

def update_pedals(state, accelerator_held, brake_held, dt):
    if brake_held:
        state.brake_percentage = min(100, state.brake_percentage + BRAKE_RISE_RATE * dt)
        state.accelerator_percentage = max(0, state.accelerator_percentage - ACCELERATOR_RELEASE_RATE * dt)
    else:
        state.brake_percentage = max(0, state.brake_percentage - BRAKE_RELEASE_RATE * dt)
        rate = ACCELERATOR_RISE_RATE if accelerator_held else -ACCELERATOR_RELEASE_RATE
        state.accelerator_percentage = clamp(state.accelerator_percentage + rate * dt, 0, 100)

def calculate_vehicle_motion(state, dt):
    speed_m_s = state.vehicle_speed_kmh / 3.6
    demand = lookup_drive_demand(state.vehicle_speed_kmh, state.accelerator_percentage)
    drive = demand * MAXIMUM_DRIVE_FORCE_N
    aero = 0.5 * AIR_DENSITY_KG_M3 * DRAG_COEFFICIENT * FRONTAL_AREA_M2 * speed_m_s**2
    rolling = VEHICLE_MASS_KG * GRAVITY_M_S2 * ROLLING_RESISTANCE_COEFFICIENT if speed_m_s > 0.01 else 0
    resistance = aero + rolling
    brake = state.brake_percentage / 100 * MAXIMUM_BRAKE_FORCE_N
    net = drive - resistance - brake
    acceleration = net / VEHICLE_MASS_KG
    speed = min(MAXIMUM_SPEED_KMH, max(0, speed_m_s + acceleration * dt) * 3.6)
    if speed <= STATIONARY_SPEED_KMH and net <= 0:
        speed, acceleration, net = 0.0, 0.0, 0.0
    return PhysicsResult(demand, drive, aero, rolling, resistance, brake, net, acceleration, speed)

def determine_operating_state(state):
    if state.brake_percentage > 0.5:
        return "BRAKING"
    if state.vehicle_speed_kmh == 0 and state.accelerator_percentage <= 0.01:
        return "STATIONARY"
    return "ACCELERATING" if state.vehicle_acceleration_m_s2 > 0.02 else "COASTING"
