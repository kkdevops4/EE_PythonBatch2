import streamlit as st
import folium
from streamlit_folium import st_folium

from services.osrm_service import OSRMService


class DashboardMap:

    def __init__(self, df):
        self.df = df

    def display_map(self):

        if self.df.empty:
            st.warning("No GPS data available.")
            return

        # Start Coordinate
        start = (
            self.df.iloc[0]["latitude"],
            self.df.iloc[0]["longitude"]
        )

        # Destination Coordinate
        end = (
            self.df.iloc[-1]["latitude"],
            self.df.iloc[-1]["longitude"]
        )

        # Create OSRM Service
        osrm = OSRMService()

        # Fetch Road Route
        route = osrm.get_route(start, end)

        # Create Map
        route_map = folium.Map(
            location=start,
            zoom_start=13
        )

        # Start Marker
        folium.Marker(
            location=start,
            popup="Trip Started",
            tooltip="Start",
            icon=folium.Icon(color="green", icon="play")
        ).add_to(route_map)

        # Destination Marker
        folium.Marker(
            location=end,
            popup="Trip Ended",
            tooltip="Destination",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(route_map)

        # Draw OSRM Road Route
        if route:

            folium.PolyLine(
                route,
                color="blue",
                weight=6,
                opacity=0.8
            ).add_to(route_map)

        else:
            st.warning("Unable to fetch route from OSRM.")

        # Map Heading
        st.subheader("🗺️ Vehicle Trip Route")

        st.caption(
            "Displays the complete vehicle route from the starting point to the destination using OSRM road routing."
        )

        # map center
        left, center, right = st.columns([1, 6, 1])

        with center:

            st_folium(
                route_map,
                width=900,
                height=550
            )

        # map legend
        st.caption("🟢 Start Location   |   🔴 Destination   |   🔵 Vehicle Route (OSRM)")
   