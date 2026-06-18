# A local car service center wants a simple system to store car details and 
# calculate the service charge based on the type of service chosen

# Create a Car class with attributes like car_name, owner and service_type, 
# add a calculate_charge() method that returns a fixed amount based on 
# service type (oil change, tyre rotation, full service), create 3 car objects and print the owner name, 
# service type and total charge for each


class Car:

    service_types = {
        "Full Service"  : 5000,
        "Oil Change"    : 1000,
        "Engine Check"  : 3000,
        "Tyre Rotation" : 2000,
        "Car Wash"      : 1500
    }

    def __init__(self,name,owner):
        self.name = name
        self.owner = owner
        self.services = []

    def add_service(self,service):
        self.services.append(service)

    def calculate_charge(self):
        total = 0

        for service in self.services:
            total = total + self.service_types[service]

        return total
    
    def display(self):
        print("Car name        :",self.name)
        print("Owner name      :",self.owner)
        
        print("\nService Types : ")
        for service in self.services:
            print(f"{service:<15} : {self.service_types[service]}")
        
        print("\n--------------------------------------")
        print("Total Charge    :",self.calculate_charge())

print()

cars = []

with open("car.txt", "r") as file:

    for line in file:

        name, owner = line.strip().split(",")

        car = Car(name,owner)
        cars.append(car)

print("\nAvailable Service :")

for service, charge in Car.service_types.items():
    print(f"{service:<13} : {charge}")

for car in cars:

    print(f"\nEnter services for {car.name} :")

    n = int(input("How many services : "))
    print("(TIP : Enter service name as above)")

    for i in range(n):

        service = input("Enter service name : ")

        car.add_service(service)

print("\nSERVICE REPORTS :- ")

for car in cars:
    print("--------------------------------------")
    print("            Car Details               ")
    print("--------------------------------------")
    car.display()
    print("--------------------------------------")
    print("\n")






















# c1 = Car("BMW","Yashraj","Full service")
# print("----------------------------------------------")
# print("                Car Details                   ")
# print("----------------------------------------------")
# c1.display()
# print("----------------------------------------------")
# print("\n")

# c2 = Car("Audi","Pruthviraj","Oil change")
# print("----------------------------------------------")
# print("                Car Details                   ")
# print("----------------------------------------------")
# c2.display()
# print("----------------------------------------------")
# print("\n")

# c3 = Car("Mercedez","Vishwaraj","Tyre rotation")
# print("----------------------------------------------")
# print("                Car Details                   ")
# print("----------------------------------------------")
# c3.display()
# print("----------------------------------------------")
# print("\n")