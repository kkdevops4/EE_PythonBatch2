# A workshop technician needs a simple system to store and display the basic details 
#of ECU modules fitted in a vehicle such as Engine ECU, ABS ECU and Airbag ECU

#Create an ECU class with attributes like ecu_id, ecu_type, manufacturer and 
#software_version, add a display_info() method to print all details neatly, create 3 
#ECU objects (Engine, ABS, Airbag) with different values and display each one, add a simple 
#is_updated() method that compares software_version against a given latest version and 
#prints whether the ECU is up to date or needs an update

class ECU:
    def __init__(self, ecu_id, manufacturer, software_version):
        self.ecu_id = ecu_id
        self.manufacturer = manufacturer
        self.software_version = software_version

    def display_info(self):
        print()
        print(f"ECU ID: {self.ecu_id}")
        print(f"Manufacturer: {self.manufacturer}")
        print(f"Software Version: {self.software_version}")
        


class Engine(ECU):
    def __init__(self, ecu_id, manufacturer, software_version):
        super().__init__(ecu_id,
                         manufacturer, software_version)
        
    def is_updated(self, latest_version):
        if self.software_version == latest_version:
            print("The ECU is up to date.")
            
        else:
            print("The ECU needs an update.")   
            


class ABS(ECU):
    def __init__(self, ecu_id, manufacturer, software_version):
        super().__init__(ecu_id,
                         manufacturer, software_version)

    def is_updated(self, latest_version):
        if self.software_version == latest_version:
            print("The ECU is up to date.")
        else:
            print("The ECU needs an update.")


class Airbag(ECU):
    def __init__(self, ecu_id, manufacturer, software_version):
        super().__init__(ecu_id,
                         manufacturer, software_version)
        
    def is_updated(self, latest_version):
        if self.software_version == latest_version:
            print("The ECU is up to date.")
        else:
            print("The ECU needs an update.")    


# Read file
with open("ECU_Details.txt") as file:
    for line in file:
        line = line.strip()

        ecu_type, data = line.split(":")

        ecu_id, manufacturer, version = [
            x.strip() for x in data.split(",")
        ]

        if ecu_type.strip() == "Engine":
            engine_ecu = Engine(ecu_id, manufacturer, version)
            engine_ecu.display_info()
            engine_ecu.is_updated("v1.2")

        elif ecu_type.strip() == "ABS":
            abs_ecu = ABS(ecu_id, manufacturer, version)
            abs_ecu.display_info()
            abs_ecu.is_updated("v1.2")

        elif ecu_type.strip() == "Airbag":
            airbag_ecu = Airbag(ecu_id, manufacturer, version)
            airbag_ecu.display_info()
            airbag_ecu.is_updated("v1.2")
