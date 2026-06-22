# Base Class
class EmissionReading:
    def get_emission(self):
        return 100  # Base emission

    def get_report(self):
        return "Base Emission: 100"


# CO2 Decorator
class CO2Decorator:
    def __init__(self, emission):
        self.emission = emission

    def get_emission(self):
        return self.emission.get_emission() + 50

    def get_report(self):
        return self.emission.get_report() + "\nCO2: 50"


# NOx Decorator
class NOxDecorator:
    def __init__(self, emission):
        self.emission = emission

    def get_emission(self):
        return self.emission.get_emission() + 30

    def get_report(self):
        return self.emission.get_report() + "\nNOx: 30"


# Particulate Decorator
class ParticulateDecorator:
    def __init__(self, emission):
        self.emission = emission

    def get_emission(self):
        return self.emission.get_emission() + 20

    def get_report(self):
        return self.emission.get_report() + "\nParticulates: 20"


# Usage
report = EmissionReading()
report = CO2Decorator(report)
report = NOxDecorator(report)
report = ParticulateDecorator(report)

print(report.get_report())
print("Total Emission Score:", report.get_emission())