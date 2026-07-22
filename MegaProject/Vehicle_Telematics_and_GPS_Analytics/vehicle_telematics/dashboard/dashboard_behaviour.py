import streamlit as st
import plotly.express as px

from analytics.driving_analysis import DrivingBehaviorAnalysis


class DashboardBehavior:

    def __init__(self, df):
        self.df = df

    def display(self):

        behavior = DrivingBehaviorAnalysis(self.df)

        summary = behavior.summary()

        st.subheader("🚗 Driving Behaviour Summary")
        st.caption("Note: Count is measured in times.")

        left_col, right_col = st.columns([1, 1])

        with left_col:

            col1, col2 = st.columns(2)

            col1.metric(
                "🟢 Normal Driving",
                summary["Normal Driving"]
            )

            col2.metric(
                "🟡 Harsh Acceleration",
                summary["Harsh Acceleration"]
            )

            col3, col4 = st.columns(2)

            col3.metric(
                "🟠 Harsh Braking",
                summary["Harsh Braking"]
            )

            col4.metric(
                "🔴 Overspeed",
                summary["Overspeed"]
            )

        with right_col:

            st.markdown("#### Driving Behaviour Distribution")
            chart_data = {
            "Behaviour": list(summary.keys()),
            "Count": list(summary.values())
            }
            
            fig = px.pie(
                chart_data,
                names="Behaviour",
                values="Count",
                hole=0.45,      # Donut chart

                color="Behaviour",

                color_discrete_map={
                    "Normal Driving": "#28a745",       # Green
                    "Harsh Acceleration": "#ffc107",   # Yellow
                    "Harsh Braking": "#fd7e14",        # Orange
                    "Overspeed":"#dc3545"             # Red
                }
            )

            fig.update_layout(
                showlegend=False,
                height=350,
                margin=dict(l=10, r=10, t=30, b=10)
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont_size=14
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
