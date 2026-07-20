

from modules import data_loader as data
from modules import threshold_processor as threshold
from modules import comparator as comp
from modules import alert_engine as alert
from modules import recommendation as recom
from modules import report_generator as report
from modules import visualization as visual


threshold_data, dummy_data = data.load_data()
# print(f"{threshold_data.head()} \n{"-"*90}\n {dummy_data.head()}")

processed_thresholds = threshold.process_threshold(threshold_data)

all_vehicle_data = []

status_counts = {
    "GREEN": 0,
    "YELLOW": 0,
    "RED": 0
}
# print((process_threshold["Engine Temperature (°C)"]))

for index, row in dummy_data.iterrows():

    # print(dummy_data.columns)
    # print(dummy_data.columns.tolist())

    statuses = []

    vehicle_id = row["Vehicle_ID"]

    engine_temp = row["Engine_Temp"]
    oil_life = row["Oil_Life"]
    oil_temp = row["Oil_Temp"]

    front_brake = row["Front_Brake"]
    rear_brake = row["Rear_Brake"]

    brake_fluid = row["Brake_Fluid_Condition"]

    battery_voltage = row["Battery_Voltage"]
    charging_voltage = row["Charging_Voltage"]

    mileage = row["Mileage"]

    rpm = row["RPM"]

    coolant_temp = row["Coolant_Temp"]

    engine_hours = row["Engine_Hours"]


    # COMPARATOR SECTION

    engine_status = comp.compare(
        engine_temp,
        processed_thresholds["Engine Temperature (°C)"]
    )

    oil_life_status = comp.compare(
        oil_life,
        processed_thresholds["Engine Oil Life (%)"]
    )

    oil_temp_status = comp.compare(
        oil_temp,
        processed_thresholds["Engine Oil Temperature (°C)"]
    )

    front_brake_status = comp.compare(
        front_brake,
        processed_thresholds["Front Brake Wear (%)"]
    )

    rear_brake_status = comp.compare(
        rear_brake,
        processed_thresholds["Rear Brake Wear (%)"]
    )

    brake_fluid_status = comp.compare(
        brake_fluid,
        processed_thresholds["Brake Fluid Condition (%)"]
    )

    battery_status = comp.compare(
        battery_voltage,
        processed_thresholds["Battery Voltage (V)"]
    )

    charging_status = comp.compare(
        charging_voltage,
        processed_thresholds["Charging Voltage (V)"]
    )

    mileage_status = comp.compare(
        mileage,
        processed_thresholds[
            "Mileage Since Last Service (km)"
        ]
    )

    rpm_status = comp.compare(
        rpm,
        processed_thresholds["Engine RPM"]
    )

    coolant_status = comp.compare(
        coolant_temp,
        processed_thresholds[
            "Coolant Temperature (°C)"
        ]
    )

    engine_hours_status = comp.compare(
        engine_hours,
        processed_thresholds["Engine Hours"]
    )

    statuses.append(engine_status)
    statuses.append(oil_life_status)
    statuses.append(oil_temp_status)
    statuses.append(front_brake_status)
    statuses.append(rear_brake_status)
    statuses.append(brake_fluid_status)
    statuses.append(battery_status)
    statuses.append(charging_status)
    statuses.append(mileage_status)
    statuses.append(rpm_status)
    statuses.append(coolant_status)
    statuses.append(engine_hours_status)    

    if "RED" in statuses:
        final_status = "RED"

    elif "YELLOW" in statuses:
        final_status = "YELLOW"

    else:
        final_status = "GREEN"


    vehicle_alert = alert.generate_alert( final_status )
    
    vehicle_recommendation = recom.generate_recommendation(final_status)


    report.generate_txt_report(
        vehicle_id,
        final_status,
        vehicle_alert,
        vehicle_recommendation
    )

    status_counts[final_status] += 1

    all_vehicle_data.append(

        {
            "Vehicle ID": vehicle_id,
            "Status": final_status,
            "Alert": vehicle_alert,
            "Recommendation":
                vehicle_recommendation
        }

    )





report.generate_excel_report(all_vehicle_data)

visual.generate_pie_chart(status_counts)

visual.generate_bar_graph(status_counts)

print("Main")



