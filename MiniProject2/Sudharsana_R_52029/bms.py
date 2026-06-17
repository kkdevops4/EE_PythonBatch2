class BatteryBMS:
    def __init__(self, voltage, temperature, charge):
        self.voltage = voltage
        self.temperature = temperature
        self.charge = charge

    #Voltage 
    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        if not (300 <= value <= 420):
            raise ValueError("Voltage out of safe range (300–420)")
        self._voltage = value

    #Temperature 
    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not (0 <= value <= 60):
            raise ValueError("Temperature out of safe range (0–60)")
        self._temperature = value

    #Charge
    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value):
        if not (0 <= value <= 100):
            raise ValueError("Charge out of safe range (0–100)")
        self._charge = value

    # Final Battery Status
    def battery_status(self, mode):

    #Running mode
        if mode == "running":

            if self.temperature > 60 or self.voltage > 415 or self.charge < 15:
                return " 🔴 CRITICAL : Battery in CRITICAL condition: Immediate action required!"

            elif (50 <= self.temperature <= 60 or
              300 <= self.voltage < 320 or
              410 <= self.voltage <= 415 or
              15 <= self.charge <= 30):
                return " 🟡 WARNING :Battery in WARNING state: monitor closely"

            else:
                return " 🟢 HEALTHY : All parameters within safe operating range"

    #charging mode
        elif mode == "charging":

            if self.temperature > 55 or self.voltage > 415 or self.charge < 10:
                return " 🔴 CRITICAL: Battery in CRITICAL condition: immediate action required!"

            elif (45 <= self.temperature <= 55 or
              400 <= self.voltage <= 415 or
              10 <= self.charge <= 20 or
              90 <= self.charge <= 100):
                return " 🟡 WARNING :Battery in WARNING state: monitor closely"

            else:
                return " 🟢 HEALTHY : All parameters within safe operating range"

    #parked mode
        elif mode == "parked":

            if self.temperature > 50 or self.voltage > 415 or self.charge < 20:
                return " 🔴 CRITICAL: Battery in CRITICAL condition: immediate action required!"

            elif (40 <= self.temperature <= 50 or
              410 <= self.voltage <= 415 or
              20 <= self.charge <= 40):
                return " 🟡 WARNING : Battery in WARNING state: monitor closely"

            else:
                return " 🟢 HEALTHY : All parameters within safe operating range"

        return "UNKNOWN MODE"

#file part
try:
    with open("battery_data.txt", "r") as file:
        voltage = float(file.readline().strip())
        temperature = float(file.readline().strip())
        charge = float(file.readline().strip())
        mode = file.readline().strip()

    battery = BatteryBMS(voltage, temperature, charge)

    print("BATTERY MANAGEMENT SYSTEM REPORT")
    print("Voltage     :", battery.voltage)
    print("Temperature :", battery.temperature)
    print("Charge      :", battery.charge)
    print("Mode        :", mode)
    print("Status      :", battery.battery_status(mode))

except FileNotFoundError:
    print("File not found!!!!")

except ValueError as e:
    print("Error:", e)