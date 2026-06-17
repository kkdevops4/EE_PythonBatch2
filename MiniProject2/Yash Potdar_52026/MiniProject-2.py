class VehicleSpeedProfile:
    def __init__(self, raw_speed_data):
        self.raw_speed_data = raw_speed_data
        self.speed_profile = []
        self.zone_profile = []

    def clean_data(self):
        for speed in self.raw_speed_data:
            if 0 <= speed <= 180:
                self.speed_profile.append(speed)

    def tag_zones(self):
        for speed in self.speed_profile:
            if speed == 0:
                self.zone_profile.append("Idle")
            elif speed <= 60:
                self.zone_profile.append("City")
            else:
                self.zone_profile.append("Highway")

    def calculate_average(self):
        total = 0
        for speed in self.speed_profile:
            total += speed

        if len(self.speed_profile) == 0:
            return 0

        return total / len(self.speed_profile)

    def display(self):
        print("Speed Profile :", self.speed_profile)
        print("Zone Tags     :", self.zone_profile)
        print("Average Speed :", round(self.calculate_average(), 2), "km/h")


raw_speed_data = []

with open("Sample_Speed.txt", "r") as file:
    for line in file:
        line = line.strip()

        if line:  
            raw_speed_data.append(int(line))

vehicle = VehicleSpeedProfile(raw_speed_data)

vehicle.clean_data()
vehicle.tag_zones()

vehicle.display()