from threshold_processor import get_status

def analyze_vehicle(vehicle_row):

    results = {}

    for column in vehicle_row.index:

        if column == "Vehicle_ID":
            continue

        value = vehicle_row[column]

        status = get_status(column, value)

        results[column] = {
            "value": value,
            "status": status
        }

    return results