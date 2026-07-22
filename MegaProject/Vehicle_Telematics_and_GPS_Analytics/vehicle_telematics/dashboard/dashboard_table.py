import streamlit as st
from analytics.driving_analysis import DrivingBehaviorAnalysis

class DashboardTable:

    def __init__(self, df):
        self.df = df

    def display_table(self):

        if self.df.empty:
            st.warning("No telemetry data available.")
            return

        # Create a copy so we don't modify the original DataFrame
        # table_df = self.df.copy()
        
        behavior = DrivingBehaviorAnalysis(self.df)

        table_df = behavior.analyze()

        # Add Serial Number
        table_df.insert(0, "Record Id.", range(1, len(table_df) + 1))

        # Round GPS coordinates
        table_df["latitude"] = table_df["latitude"].round(6)
        table_df["longitude"] = table_df["longitude"].round(6)

        # Round values
        table_df["speed"] = table_df["speed"].round(1)
        table_df["fuel_level"] = table_df["fuel_level"].round(2)
        table_df["engine_temp"] = table_df["engine_temp"].round(1)

        # Rename columns for display
        table_df = table_df.rename(columns={
            "timestamp": "Timestamp",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "speed": "Speed (km/h)",
            "fuel_level": "Fuel (%)",
            "engine_temp": "Engine Temp (°C)",

            "Driving Behavior": "Driving Behavior"
        })

        st.subheader("📋 Telemetry Data")

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True
        )