import streamlit as st
from analytics.trip_analysis import TripAnalysis


class DashboardMetrics:

    def __init__(self, df):
        self.df = df

    def display_metrics(self):

        if self.df.empty:
            st.warning("No telemetry data available.")
            return

        # Latest telemetry record
        latest_record = self.df.iloc[-1]

        # Calculate total distance
        trip = TripAnalysis(self.df)
        total_distance = trip.total_distance()

        # Create four metric cards
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "🚗 Current Speed",
            f"{latest_record['speed']} km/h"
        )

        col2.metric(
            "⛽ Fuel Level",
            f"{latest_record['fuel_level']} %"
        )

        col3.metric(
            "🌡️ Engine Temperature",
            f"{latest_record['engine_temp']} °C"
        )

        col4.metric(
            "📍 Distance Travelled",
            f"{total_distance} km"
        )