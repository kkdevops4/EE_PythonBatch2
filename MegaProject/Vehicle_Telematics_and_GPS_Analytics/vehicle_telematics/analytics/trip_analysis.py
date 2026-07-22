from math import radians, sin, cos, sqrt, atan2


class TripAnalysis:

    def __init__(self, df):                                     # DataFrame df is taken here from dashboard loader
        self.df = df

    # Private Method
    def _haversine_distance(self, lat1, lon1, lat2, lon2):

        R = 6371  # Earth Radius in KM

        lat1 = radians(lat1)
        lon1 = radians(lon1)

        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            sin(dlat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(dlon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    # Total Distance
    def total_distance(self):

        if len(self.df) < 2:
            return 0

        distance = 0

        for i in range(1, len(self.df)):

            previous = self.df.iloc[i - 1]
            current = self.df.iloc[i]

            distance += self._haversine_distance(
                previous["latitude"],
                previous["longitude"],
                current["latitude"],
                current["longitude"],
            )

        return round(distance, 2)

    # Average Speed
    def average_speed(self):

        if self.df.empty:
            return 0

        return round(self.df["speed"].mean(), 2)

    # Maximum Speed
    def maximum_speed(self):

        if self.df.empty:
            return 0

        return self.df["speed"].max()

    # Fuel Consumed
    def fuel_consumed(self):

        if self.df.empty:
            return 0

        start_fuel = self.df.iloc[0]["fuel_level"]
        end_fuel = self.df.iloc[-1]["fuel_level"]

        return round(start_fuel - end_fuel, 2)

    # Trip Duration
    def trip_duration(self):

        start = self.df.iloc[0]["timestamp"]
        end = self.df.iloc[-1]["timestamp"]

        duration = end - start

        # Convert duration to total seconds
        total_seconds = int(duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"