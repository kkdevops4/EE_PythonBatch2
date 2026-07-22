class FuelAnalysis:

    def __init__(self, dataframe):
        self.df = dataframe

    def current_fuel(self):
        return round(self.df["fuel_level"].iloc[-1], 2)

    def fuel_consumed(self):
        start = self.df["fuel_level"].iloc[0]
        end = self.df["fuel_level"].iloc[-1]

        return round(start - end, 2)