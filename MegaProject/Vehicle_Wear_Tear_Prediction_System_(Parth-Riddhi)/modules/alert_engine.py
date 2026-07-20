

def generate_alert(status) :
    if status == "GREEN":
        return("Vehicle Healthy")

    elif status == "YELLOW" :
        return("Service Recommended")

    elif status == "RED" :
        return("Immediate Service Required")

    elif status == "INVALID" :
        return("Invalid Sensor Data")

    else:
        return("Unknown Status")

