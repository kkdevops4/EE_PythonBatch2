class EngineAnalysis:

    def __init__(self, dataframe):
        self.df = dataframe

    def current_temperature(self):
        return self.df["engine_temp"].iloc[-1]

    def maximum_temperature(self):
        return self.df["engine_temp"].max()

    def minimum_temperature(self):
        return self.df["engine_temp"].min()