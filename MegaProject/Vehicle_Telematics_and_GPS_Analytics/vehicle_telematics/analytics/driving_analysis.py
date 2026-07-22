class DrivingBehaviorAnalysis:

    def __init__(self, df):
        self.df = df.copy()

    def analyze(self):

        behaviors = []

        previous_speed = None

        for speed in self.df["speed"]:

            if previous_speed is None:
                behaviors.append("Normal Driving")

            else:

                difference = speed - previous_speed

                if speed > 80:
                    behaviors.append("Overspeed")

                elif difference >= 8:
                    behaviors.append("Harsh Acceleration")

                elif difference <= -8:
                    behaviors.append("Harsh Braking")

                else:
                    behaviors.append("Normal Driving")

            previous_speed = speed

        self.df["Driving Behavior"] = behaviors

        return self.df
    
    def summary(self):

        df = self.analyze()

        return {
            "Normal Driving": (df["Driving Behavior"] == "Normal Driving").sum(),
            "Harsh Acceleration": (df["Driving Behavior"] == "Harsh Acceleration").sum(),
            "Harsh Braking": (df["Driving Behavior"] == "Harsh Braking").sum(),
            "Overspeed": (df["Driving Behavior"] == "Overspeed").sum()
        }