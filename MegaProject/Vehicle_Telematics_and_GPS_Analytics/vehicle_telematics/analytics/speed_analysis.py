class SpeedAnalysis:

    def __init__(self, dataframe):
        self.df = dataframe

    def current_speed(self):
        return self.df["speed"].iloc[-1]

    def average_speed(self):
        return round(self.df["speed"].mean(), 2)

    def maximum_speed(self):
        return self.df["speed"].max()

    def minimum_speed(self):
        return self.df["speed"].min()