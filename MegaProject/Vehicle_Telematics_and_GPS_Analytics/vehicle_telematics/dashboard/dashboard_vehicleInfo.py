import streamlit as st


class DashboardVehicleInfo:

    def display(self):

        st.subheader("🚗 Vehicle Information")

        left_col, right_col = st.columns(2)

        with left_col:

            st.markdown("**Vehicle ID**")
            st.write("CAR001")

            st.markdown("**Manufacturer**")
            st.write("Tata Nexon")

            st.markdown("**Model**")
            st.write("Nexon")

            st.markdown("**Vehicle Type**")
            st.write("SUV")

        with right_col:

            st.markdown("**Registration Number**")
            st.write("MH09 AB 1234")

            st.markdown("**Fuel Type**")
            st.write("Petrol")

            st.markdown("**Model Year**")
            st.write("2024")

            st.markdown("**Driver Name**")
            st.write("Yash Patil")
