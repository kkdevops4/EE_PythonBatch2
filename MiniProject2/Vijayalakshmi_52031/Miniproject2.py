
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year



class Car(Vehicle):
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def display_info(self):
        print("Car Details:")
        print(f"Name (Make): {self.make}")
        print(f"Model       : {self.model}")
        print(f"Year        : {self.year}")
        print(f"No. of Doors: {self.num_doors}")
        print("-" * 30)

class Bike(Vehicle):
    def __init__(self, make, model, year, bike_type):
        super().__init__(make, model, year)
        self.bike_type = bike_type

    def display_info(self):
        print("Bike Details:")
        print(f"Name (Make): {self.make}")
        print(f"Model       : {self.model}")
        print(f"Year        : {self.year}")
        print(f"Type        : {self.bike_type}")
        print("-" * 30)



with open("vehicles.txt", "r") as file:
    for line in file:
        data = line.strip().split(",")

        if data[0] == "Car":
            car = Car(data[1], data[2], int(data[3]), int(data[4]))
            car.display_info()

        elif data[0] == "Bike":
            bike = Bike(data[1], data[2], int(data[3]), data[4])
            bike.display_info()



