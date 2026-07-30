

from modules import data_loader as data
from modules import threshold_processor as threshold
from modules import comparator as comp
from modules import alert_engine as alert
from modules import recommendation as recom
from modules import report_generator as report
from modules import visualization as visual


(threshold_data, dummy_data, owner_data, vehicle_data,service_data ) = data.load_data()
# print(f"{threshold_data.head()} \n{"-"*90}\n {dummy_data.head()}")

processed_thresholds = threshold.process_threshold(threshold_data)

# all_vehicle_data = []

# status_counts = {
#     "GREEN": 0,
#     "YELLOW": 0,
#     "RED": 0
# }
# print((process_threshold["Engine Temperature (°C)"]))

print("\nAvailable Vehicle Numbers\n")

for number in vehicle_data["Vehicle_Number"]:

    print(number)

while True:

    vehicle_number = input(
        "\nEnter Vehicle Number : "
    ).upper()

    selected_vehicle = vehicle_data[
        vehicle_data["Vehicle_Number"] == vehicle_number
    ]

    if not selected_vehicle.empty:

        break

    print(
        "\nInvalid Vehicle Number!"
    )

    print(
        "Please select from the list above."
    )

vehicle_row = selected_vehicle.iloc[0]

vehicle_id = vehicle_row["Vehicle_ID"]

# for index, row in dummy_data.iterrows():


row = dummy_data[
    dummy_data["Vehicle_ID"] == vehicle_id].iloc[0]

    # print(dummy_data.columns)
    # print(dummy_data.columns.tolist())

statuses = []
sensor_statuses = {}
sensor_values = {}

# vehicle_id = row["Vehicle_ID"]



owner_row = owner_data[
    owner_data["Vehicle_ID"] == vehicle_id
].iloc[0]

vehicle_row = vehicle_data[
    vehicle_data["Vehicle_ID"] == vehicle_id
].iloc[0]

vehicle_info = {

    "Vehicle Number": vehicle_row["Vehicle_Number"],

    "Owner Name": owner_row["Owner_Name"],

    "Contact Number": owner_row["Contact_Number"],

    "Model": vehicle_row["Model"],

    "Fuel Type": vehicle_row["Fuel_Type"],

    "Color": vehicle_row["Color"],

    "Manufacturing Year": vehicle_row["Manufacturing_Year"],

    "Registration Date": vehicle_row["Registration_Date"]
}

engine_temp = row["Engine Temperature (°C)"]
oil_life = row["Engine Oil Life (%)"]
oil_temp = row["Engine Oil Temperature (°C)"]

front_brake = row["Front Brake Wear (%)"]
rear_brake = row["Rear Brake Wear (%)"]

brake_fluid = row["Brake Fluid Condition (%)"]

battery_voltage = row["Battery Voltage (V)"]
charging_voltage = row["Charging Voltage (V)"]

mileage = row["Mileage Since Last Service (km)"]

rpm = row["Engine (Rotations Per Minute)"]

coolant_temp = row["Coolant Temperature (°C)"]

engine_hours = row["Engine (Hours)"]


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
    processed_thresholds["Engine (Rotations Per Minute)"]
)

coolant_status = comp.compare(
    coolant_temp,
    processed_thresholds[
        "Coolant Temperature (°C)"
    ]
)

engine_hours_status = comp.compare(
    engine_hours,
    processed_thresholds["Engine (Hours)"]
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

sensor_statuses = {
                    "Engine Temperature" : engine_status,
                    "Engine Oil Life" : oil_life_status,
                    "Engine Oil Temperature" : oil_temp_status,
                    "Front Brake Wear" : front_brake_status,
                    "Rear Brake Wear" : rear_brake_status,
                    "Brake Fluid Condition" : brake_fluid_status,
                    "Battery Voltage" : battery_status,
                    "Charging Voltage" : charging_status,
                    "Mileage Since Last Service" : mileage_status,
                    "Engine RPM" : rpm_status,
                    "Coolant Temperature" : coolant_status,
                    "Engine Hours" : engine_hours_status}


recommendation = recom.generate_recommendation(sensor_statuses)    
# print("Recommendation :- \n",recommendation)

sensor_values = {
    "Engine Temperature" : engine_temp,
    "Engine Oil Life" : oil_life,
    "Engine Oil Temperature" : oil_temp,
    "Front Brake Wear" : front_brake,
    "Rear Brake Wear" : rear_brake,
    "Brake Fluid Condition" :brake_fluid,
    "Battery Voltage" : battery_voltage,
    "Charging Voltage" : charging_voltage,
    "Mileage Since Last Service" : mileage,
    "Engine RPM" : rpm,
    "Coolant Temperature" : coolant_temp,
    "Engine Hours" : engine_hours }


# FINAL STATUS
if "RED" in statuses:
    final_status = "RED"

elif "YELLOW" in statuses:
    final_status = "YELLOW"

else:
    final_status = "GREEN"


vehicle_alert = alert.generate_alert(final_status)

status_counts, status_sensors = visual.prepare_status_summary(sensor_statuses)

visual.generate_pie_chart(
    status_counts,status_sensors)


# visual.generate_bar_graph(count)


report.generate_pdf_report(vehicle_info,sensor_values,sensor_statuses,recommendation,final_status,vehicle_alert)

print(
    f"\nPDF Report Generated : "
    f"reports/{vehicle_number}.pdf")

'''
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

'''


