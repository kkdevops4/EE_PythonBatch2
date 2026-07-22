def get_status(parameter, value):

    thresholds = {

    "Engine Temperature (°C)": {
        "green": (70, 95),
        "yellow": (96, 105)
    },

    "Engine Oil Life (%)": {
        "green": (60, 100),
        "yellow": (30, 60)
    },

    "Engine Oil Temperature (°C)": {
        "green": (90, 110),
        "yellow": (111, 120)
    },

    "Front Brake Wear (%)": {
        "green": (0, 50),
        "yellow": (51, 80)
    },

    "Rear Brake Wear (%)": {
        "green": (0, 50),
        "yellow": (51, 80)
    },

    "Brake Fluid Condition (%)": {
        "green": (70, 100),
        "yellow": (40, 70)
    },

    "Battery Voltage (V)": {
        "green": (12.4, 14.0),
        "yellow": (12.0, 12.3)
    },

    "Charging Voltage (V)": {
        "green": (13.5, 14.5),
        "yellow": (12.5, 13.4)
    },

    "Mileage Since Last Service (km)": {
        "green": (0, 8000),
        "yellow": (8001, 10000)
    },

    "Engine (Rotations Per Minute)": {
        "green": (800, 3500),
        "yellow": (3501, 4500)
    },

    "Coolant Temperature (°C)": {
        "green": (80, 95),
        "yellow": (96, 105)
    },

    "Engine (Hours)": {
        "green": (0, 2000),
        "yellow": (2001, 3500)
    }
}

    rule = thresholds.get(parameter)

    if rule is None:
        print(f"Parameter not found: {parameter}")
        return "UNKNOWN"

    green_min, green_max = rule["green"]
    yellow_min, yellow_max = rule["yellow"]

    if green_min <= value <= green_max:
        return "GREEN"

    elif yellow_min <= value <= yellow_max:
        return "YELLOW"

    else:
        return "RED"