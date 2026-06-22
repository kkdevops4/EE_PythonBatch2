# Base Class
class EmissionReading:
    def __init__(self, emission):
        self.emission = emission

    def get_emission(self):
        return self.emission

    def get_report(self):
        return "Base Emission: " + str(self.emission)


# CO2 Decorator
class CO2Decorator:
    def __init__(self, emission, co2):
        self.emission = emission
        self.co2 = co2

    def get_emission(self):
        return self.emission.get_emission() + self.co2

    def get_report(self):
        return self.emission.get_report() + "\nCO2: " + str(self.co2)


# NOx Decorator
class NOxDecorator:
    def __init__(self, emission, nox):
        self.emission = emission
        self.nox = nox

    def get_emission(self):
        return self.emission.get_emission() + self.nox

    def get_report(self):
        return self.emission.get_report() + "\nNOx: " + str(self.nox)


# Particulate Decorator
class ParticulateDecorator:
    def __init__(self, emission, particulate):
        self.emission = emission
        self.particulate = particulate

    def get_emission(self):
        return self.emission.get_emission() + self.particulate

    def get_report(self):
        return self.emission.get_report() + "\nParticulates: " + str(self.particulate)


# User Input
base = int(input("Enter Base Emission: "))
co2 = int(input("Enter CO2 Value: "))
nox = int(input("Enter NOx Value: "))
particulate = int(input("Enter Particulate Value: "))

# Apply Decorators
report = EmissionReading(base)
report = CO2Decorator(report, co2)
report = NOxDecorator(report, nox)
report = ParticulateDecorator(report, particulate)

# Output
print("\nEmission Report")
print(report.get_report())
print("Total Emission Score:", report.get_emission())