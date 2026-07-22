import random
from datetime import datetime


class TelemetryGenerator:
    def __init__(self):
        # Initial vehicle values
        self.start_lat = 18.5204
        self.start_lon = 73.8567

        self.latitude = self.start_lat
        self.longitude = self.start_lon

        # Random Destination
        self.destination_lat = self.start_lat + random.uniform(-0.06, 0.06)
        self.destination_lon = self.start_lon + random.uniform(-0.06, 0.06)

        # Total Telemetry Records
        self.total_records = random.randint(20, 30)
        self.current_record = 0

         # GPS Movement Per Record
        self.lat_step = (
            self.destination_lat - self.start_lat
        ) / self.total_records

        self.lon_step = (
            self.destination_lon - self.start_lon
        ) / self.total_records

        self.speed = random.randint(20, 30)

        # Random maximum cruising speed for this trip
        self.cruise_speed = random.randint(70, 95)

        self.fuel_level = 100.0      # Start with full tank

        # self.engine_temp = 70        # Engine just started
        self.engine_temp = random.uniform(25, 35)


    def generate_data(self):

        self.current_record += 1

        # Current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # Move towards destination
        self.latitude += self.lat_step
        self.longitude += self.lon_step

        # Random speed
        # First 30% of trip -> Accelerate
        if self.current_record <= self.total_records * 0.3:

            speed_change = random.randint(4, 8)
            self.speed += speed_change

            # Don't exceed cruise speed while accelerating
            if self.speed > self.cruise_speed:
                self.speed = self.cruise_speed


        # Middle 40% of trip -> Cruise
        elif self.current_record <= self.total_records * 0.7:

            self.speed += random.randint(-2, 2)

            # Stay close to cruise speed
            if self.speed > self.cruise_speed + 2:
                self.speed = self.cruise_speed + 2

            if self.speed < self.cruise_speed - 2:
                self.speed = self.cruise_speed - 2


        # Last 30% of trip -> Slow down
        else:
            self.speed -= random.randint(4, 8)

        # Keep speed within limits
        self.speed = max(20, min(100, self.speed))

        # Fuel decreases slowly
        fuel_drop = random.uniform(0.03, 0.08)
        self.fuel_level -= fuel_drop
        self.fuel_level = max(0, self.fuel_level)

        # engine temperature
        if self.speed <= 30:
            target_temp = random.uniform(30, 40)

        elif self.speed <= 50:
            target_temp = random.uniform(40, 65)

        else:
            target_temp = random.uniform(65, 90)

        # Move gradually towards the target temperature
        if self.engine_temp < target_temp:
            self.engine_temp += random.uniform(0.5, 1.5)

        elif self.engine_temp > target_temp:
            self.engine_temp -= random.uniform(0.2, 0.8)

        # Keep temperature within safe limits
        self.engine_temp = max(20, min(95, self.engine_temp))
        

        telemetry = {
            "timestamp": timestamp,
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6),
            "speed": self.speed,
            "fuel_level": round(self.fuel_level, 2),
            "engine_temp": round(self.engine_temp, 1)
        }

        return telemetry