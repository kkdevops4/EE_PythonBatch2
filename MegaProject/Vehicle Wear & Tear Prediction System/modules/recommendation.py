

def generate_recommendation(sensor_statuses):

    recommendation_data = {
        "Engine Temperature" : 
        {"GREEN":
            "Engine temperature is operating within normal range.",

        "YELLOW":
            "Monitor engine temperature and schedule cooling system inspection.",

        "RED":
            "Immediate cooling system diagnosis required."
        },

        "Engine Oil Life" : {
        "GREEN":
            "Engine oil condition is healthy.",

        "YELLOW":
            "Plan engine oil replacement soon.",

        "RED":
            "Replace engine oil immediately."},


    "Engine Oil Temperature" : {
        "GREEN":
            "Engine oil temperature is normal.",

        "YELLOW":
            "Monitor oil temperature during operation.",

        "RED":
            "Inspect lubrication system immediately."},


    "Front Brake Wear" : {
        "GREEN":
            "Front brake condition is good.",

        "YELLOW":
            "Schedule front brake inspection.",

        "RED":
            "Replace front brake components immediately."},


    "Rear Brake Wear" : {
        "GREEN":
            "Rear brake condition is good.",

        "YELLOW":
            "Schedule rear brake inspection.",

        "RED":
            "Replace rear brake components immediately." },


    "Brake Fluid Condition" : {
        "GREEN":
            "Brake fluid condition is satisfactory.",

        "YELLOW":
            "Check brake fluid quality during next service.",

        "RED":
            "Replace brake fluid immediately."},


    "Battery Voltage" : {
        "GREEN":
            "Battery health is normal.",

        "YELLOW":
            "Monitor battery performance and charging system.",

        "RED":
            "Inspect or replace battery immediately."},


    "Charging Voltage" : {
        "GREEN":
            "Charging system is functioning correctly.",

        "YELLOW":
            "Inspect alternator and charging system.",

        "RED":
            "Immediate charging system diagnosis required."},


    "Mileage Since Last Service" : {
        "GREEN":
            "Vehicle service schedule is up to date.",

        "YELLOW":
            "Schedule routine maintenance soon.",

        "RED":
            "Vehicle service is overdue."},


    "Engine RPM" : {
        "GREEN":
            "Engine RPM is within normal operating range.",

        "YELLOW":
            "Monitor engine performance and RPM fluctuations.",

        "RED":
            "Inspect engine operation immediately."},


    "Coolant Temperature" : {
        "GREEN":
            "Coolant temperature is normal.",

        "YELLOW":
            "Check coolant level and cooling efficiency.",

        "RED":
            "Immediate cooling system inspection required."},


    "Engine Hours" : {
        "GREEN":
            "Engine operating hours are within expected limits.",

        "YELLOW":
            "Plan preventive maintenance based on engine usage.",

        "RED":
            "Engine requires immediate maintenance due to excessive usage."}
    }

    recommendations = []

    for sensor,status in sensor_statuses.items() :
        # print(sensor)
        # print(status)

        recommendation = recommendation_data[sensor][status]
        recommendations.append(f"{sensor} : {recommendation}")


    return recommendations






        # print("sensor := ",recommendation_data[sensor])
        # print("Sensor - status : -",sensor)
        # print()
