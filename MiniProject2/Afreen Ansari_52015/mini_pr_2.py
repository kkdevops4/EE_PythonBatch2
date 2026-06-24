# Base Car Class
class Car:
    def __init__(self, model, price):
        self.model = model
        self.price = price

    def get_description(self):
        return self.model + " Base Model"

    def get_price(self):
        return self.price

    def get_features(self):
        return []


# Base Decorator
class CarDecorator:
    def __init__(self, car, cost, name):
        self.car = car
        self.cost = cost
        self.name = name

    def get_description(self):
        return self.car.get_description() + " + " + self.name

    def get_price(self):
        return self.car.get_price() + self.cost

    def get_features(self):
        return self.car.get_features() + [self.name]


# Individual Decorators
class Sunroof(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Sunroof")


class Navigation(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Navigation")


class LeatherSeats(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Leather Seats")


class HeatedSeats(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Heated Seats")


class ParkingSensors(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Parking Sensors")


class PremiumSound(CarDecorator):
    def __init__(self, car, cost):
        super().__init__(car, cost, "Premium Sound")


# Read data from file
file = open("input.txt", "r")

data = {}
for line in file:
    line = line.strip()

    if line != "":
        key, value = line.split("=")
        data[key] = value

file.close()

# Create base car
model = data["Model"]
base_price = int(data["BasePrice"])

car = Car(model, base_price)

# Available Features
features = {
    1: ("Sunroof", Sunroof),
    2: ("Navigation", Navigation),
    3: ("LeatherSeats", LeatherSeats),
    4: ("HeatedSeats", HeatedSeats),
    5: ("ParkingSensors", ParkingSensors),
    6: ("PremiumSound", PremiumSound)
}

print("=" * 60)
print("VEHICLE CONFIGURATION BUILDER")
print("=" * 60)

print("\nModel :", model)
print("Base Price : ${}".format(base_price))

print("\nAvailable Features:\n")

for num, (name, cls) in features.items():
    print(num, ".", name, "($" + data[name] + ")", sep="")

choice = input(
    "\nEnter feature numbers separated by commas (e.g. 1,3,5): "
)

selected = choice.split(",")

# Apply decorators
for item in selected:
    item = int(item.strip())

    name, decorator_class = features[item]

    car = decorator_class(car, int(data[name]))

# Final Output
print("\n" + "=" * 60)
print("FINAL CONFIGURATION")
print("=" * 60)

print("\nModel:", model)

print("\nDescription:")
print(car.get_description())

print("\nPrice: ${:,.2f}".format(car.get_price()))

print("\nFeatures:")
print(", ".join(car.get_features()))

print("\nTotal Features Added:", len(car.get_features()))

print("\n" + "=" * 60)
print("Configuration Completed Successfully!")
print("=" * 60)