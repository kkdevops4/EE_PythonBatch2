

def generate_recommendation(status):

    if status == "GREEN":
        return "No Maintenance Required"

    elif status == "YELLOW":
        return "Schedule Service Within 7 Days"

    elif status == "RED":
        return "Immediate Vehicle Inspection Required"

    elif status == "INVALID":
        return "Verify Sensor Data"

    else:
        return "Unknown Status"

