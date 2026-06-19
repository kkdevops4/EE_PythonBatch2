"""
Input file format, one vehicle per line:
    vehicle_id  distance_km  time_minutes  odometer_km  fuel_litres

Example:
    1 120 90 15032 8
"""

class Vehicle:
    """A simple class to hold one vehicle's data and basic calculations."""

    def __init__(self, vehicle_id, distance, minutes, odometer, fuel):
        self.vehicle_id = vehicle_id
        self.distance = distance
        self.minutes = minutes
        self.odometer = odometer
        self.fuel = fuel

    def get_efficiency(self):
        """Return fuel efficiency in km per litre."""
        if self.fuel == 0:
            return 0
        return round(self.distance / self.fuel, 2)

    def get_category(self):
        """Return the efficiency category based on km/l."""
        eff = self.get_efficiency()
        if eff >= 15:
            return "Excellent"
        elif eff >= 10:
            return "Good"
        elif eff >= 5:
            return "Average"
        else:
            return "Poor"

    def show(self):
        """Print vehicle details in a readable way."""
        print(f"  Vehicle {self.vehicle_id}: {self.distance} km, "
              f"{self.fuel} L -> {self.get_efficiency()} km/l "
              f"({self.get_category()})")


def read_vehicles_from_file(filename):
   
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # skip empty lines and comment lines
            if line == "" or line.startswith("#"):
                continue

            values = line.split()
            vehicle_id = int(values[0])
            distance = float(values[1])
            minutes = float(values[2])
            odometer = float(values[3])
            fuel = float(values[4])

            yield Vehicle(vehicle_id, distance, minutes, odometer, fuel)



def main():
    # Step 1: use the generator once to load all vehicles into a list
    vehicles = list(read_vehicles_from_file("vehicle_data.txt"))

    # Step 2: group vehicles by category using a plain dictionary
    groups = {"Excellent": [], "Good": [], "Average": [], "Poor": []}

    for vehicle in vehicles:
        category = vehicle.get_category()
        groups[category].append(vehicle)

    # Step 3: print the report
    print("===== VEHICLE EFFICIENCY REPORT =====")
    for category in groups:
        print(f"\n{category}: ({len(groups[category])} vehicle(s))")
        for vehicle in groups[category]:
            vehicle.show()

    print(f"\nTotal vehicles processed: {len(vehicles)}")


if __name__ == "__main__":
    main()
