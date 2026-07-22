import streamlit as st
import plotly.express as px


class DashboardCharts:

    def __init__(self, df):
        self.df = df

    def display_charts(self):

        if self.df.empty:
            st.warning("No telemetry data available.")
            return

        # create two coulumns
        col1, col2 = st.columns(2)

        # Speed Chart
        speed_fig = px.line(
            self.df,
            x="timestamp",
            y="speed",
            title="Speed vs Time",
            markers=True
        )

        speed_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Speed (km/h)"
        )

        col1.plotly_chart(speed_fig, use_container_width=True)

        # Fuel Chart
        fuel_fig = px.line(
            self.df,
            x="timestamp",
            y="fuel_level",
            title="Fuel Level vs Time",
            markers=True
        )

        fuel_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Fuel Level (%)"
        )

        col2.plotly_chart(fuel_fig, use_container_width=True)

        # Engine Temperature Chart
        temp_fig = px.line(
            self.df,
            x="timestamp",
            y="engine_temp",
            title="Engine Temperature vs Time",
            markers=True
        )

        temp_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)"
        )

        st.plotly_chart(temp_fig, use_container_width=True)