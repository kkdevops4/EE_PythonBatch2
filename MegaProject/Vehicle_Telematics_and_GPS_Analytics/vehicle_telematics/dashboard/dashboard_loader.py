import pandas as pd

from firebase.firebase_read import FirebaseReader


class DashboardLoader:

    def __init__(self):
        self.reader = FirebaseReader()

    def load_data(self):

        telemetry = self.reader.get_all_telemetry()

        if len(telemetry) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(telemetry)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        df = df.sort_values(by="timestamp")

        df.reset_index(drop=True, inplace=True)

        return df