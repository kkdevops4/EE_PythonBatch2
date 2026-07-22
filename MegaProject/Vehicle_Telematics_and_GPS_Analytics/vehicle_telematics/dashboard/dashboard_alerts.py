import streamlit as st


class DashboardAlerts:

    def __init__(self, df):
        self.df = df

    def display_alerts(self):

        st.subheader("🚨 Vehicle Alerts")

        alert_found = False

        # Overspeed Alert
        max_speed = self.df["speed"].max()

        overspeed_events = (self.df["speed"] > 80).sum()

        if overspeed_events > 0:

            st.error(
                f"""
                🚨 Overspeed Detected
                Maximum Speed : {max_speed} km/h
                Overspeed Events : {overspeed_events}
                """
            )

            alert_found = True

        # Engine Temperature Alert
        max_temp = self.df["engine_temp"].max()

        if max_temp > 90:

            st.warning(
                f"""
                🌡 High Engine Temperature
                Maximum Temperature : {max_temp:.1f} °C
                 """
            )
            alert_found = True

        # no alert
        if not alert_found:
            st.success("✅ No Alerts Generated During This Trip")