# new code
import time

from simulator.telemetry_generator import TelemetryGenerator
from firebase.firebase_service import FirebaseService

vehicle = TelemetryGenerator()
firebase = FirebaseService()

# Clear previous trip data
firebase.clear_previous_telemetry()

print("\n========== TRIP STARTED ==========\n")

print(f"Start Location : ({vehicle.start_lat}, {vehicle.start_lon})")
# print(f"Destination    : ({round(vehicle.destination_lat,6)}, {round(vehicle.destination_lon,6)})")

print("----------------------------------------")

for i in range(vehicle.total_records):

    telemetry = vehicle.generate_data()

    print(f"\nTelemetry Record {i+1}")
    print(telemetry)

    firebase.upload_telemetry(telemetry)

    time.sleep(10)

print("\n========== DESTINATION REACHED ==========")
print("Trip Completed Successfully.")