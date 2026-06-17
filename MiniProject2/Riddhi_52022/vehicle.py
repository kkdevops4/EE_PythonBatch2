import json
import os
import re


class Vehicle:
    def __init__(self, vin, company, model, year, color):
        self.vin = vin
        self.company = company
        self.model = model
        self.year = year
        self.color = color

    def to_dict(self):
        return self.__dict__ # stores an object's writable attributes in the form of a dictionary


class VehicleDB:
    FILE = "vehicles.json"

    def __init__(self):
        if not os.path.exists(self.FILE):
            with open(self.FILE, "w") as f: #with expression as variable.
                json.dump({}, f)

    def load(self):
        with open(self.FILE, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.FILE, "w") as f:
            json.dump(data, f, indent=4)

    def add(self, vehicle):
        data = self.load()
        if vehicle.vin in data:
            raise ValueError("VIN already exists.")
        data[vehicle.vin] = vehicle.to_dict()
        self.save(data)

    def get(self, vin):
        return self.load().get(vin)

    def update(self, vin, updates):
        data = self.load()
        if vin not in data:
            raise ValueError("VIN not found.")
        data[vin].update(updates)
        self.save(data)

    def delete(self, vin):
        data = self.load()
        if vin not in data:
            raise ValueError("VIN not found.")
        del data[vin]
        self.save(data)

class VIN:
    @staticmethod #decorator-A static method does not take self or cls and cannot access instance or class attributes unless explicitly passed.
    def validate(vin):
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", vin):
            raise ValueError("Invalid VIN.")
        return vin

class App:
    def __init__(self):
        self.db = VehicleDB()

    def run(self):
        while True:
            print("\n1. Add\n2. Retrieve\n3. Update\n4. Delete\n5. Exit")
            choice = input("Choice: ")

            try:
                if choice == "1":
                    self.add()
                elif choice == "2":
                    self.retrieve()
                elif choice == "3":
                    self.update()
                elif choice == "4":
                    self.delete()
                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print("Error:", e)

    def add(self):
        vin = VIN.validate(input("VIN: ").upper())
        company = input("Company: ")
        model = input("Model: ")
        year = input("Year: ")
        color = input("Color: ")

        self.db.add(Vehicle(vin, company, model, year, color))
        print("Added.")

    def retrieve(self):
        vin = input("VIN: ").upper()
        vehicle = self.db.get(vin)
        print(vehicle if vehicle else "Not found.")

    def update(self):
        vin = VIN.validate(input("VIN: ").upper())
        print("Press Enter key to skip.")
        updates = {}

        for field in ["company", "model", "year", "color"]:
            val = input(f"New {field}: ")
            if val:
                updates[field] = val

        self.db.update(vin, updates)
        print("Updated.")

    def delete(self):
        vin = VIN.validate(input("VIN: ").upper())
        self.db.delete(vin)
        print("Deleted.")


if __name__ == "__main__":
    App().run()
