import streamlit as st

from streamlit_autorefresh import st_autorefresh
from dashboard_loader import DashboardLoader
from dashboard_metrics import DashboardMetrics
from dashboard_charts import DashboardCharts
from dashboard.dashboard_map import DashboardMap
from dashboard.dashboard_table import DashboardTable
from dashboard.dashboard_behaviour import DashboardBehavior
from dashboard.dashboard_alerts import DashboardAlerts
from dashboard.dashboard_sos import DashboardSOS
from dashboard.dashboard_vehicleInfo import DashboardVehicleInfo

st.set_page_config(
    page_title="Vehicle Telematics Dashboard",
    page_icon="🚗",
    layout="wide"
)

# auto refresh
st_autorefresh(
    interval=10000,   # 10000 milliseconds = 10 seconds
    key="dashboard_refresh"
)
st.divider()

# Page heading
st.markdown(
    """
    <h1 style='text-align: center;'>
        🚘 Vehicle Telematics Dashboard
    </h1>

    <h4 style='text-align: center; color: gray;'>
        Real-Time Vehicle Monitoring & Trip Analysis
    </h4>
    """,
    unsafe_allow_html=True
)
st.divider()

loader = DashboardLoader()
df = loader.load_data()

# Vehicle Info
vehicle = DashboardVehicleInfo()
vehicle.display()

st.divider()

# metrics(KPI - key performance interface)
metrics = DashboardMetrics(df)
metrics.display_metrics()
st.divider()

# charts
charts = DashboardCharts(df)
charts.display_charts()
st.divider()

# map
dashboard_map = DashboardMap(df)
dashboard_map.display_map()
st.divider()

# trip summary
from analytics.trip_analysis import TripAnalysis

trip = TripAnalysis(df)

st.subheader("📊 Trip Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Speed",
    f"{trip.average_speed()} km/h"
)

col2.metric(
    "Maximum Speed",
    f"{trip.maximum_speed()} km/h"
)

col3.metric(
    "Fuel Consumed",
    f"{trip.fuel_consumed()} %"
)

col4.metric(
    "Trip Duration",
    trip.trip_duration()
)
st.divider()

# Trip behaviour
behavior = DashboardBehavior(df)
behavior.display()
st.divider()

# table
table = DashboardTable(df)
table.display_table()

st.divider()

alerts = DashboardAlerts(df)
alerts.display_alerts()

st.divider()

sos = DashboardSOS()
sos.display()
st.divider()