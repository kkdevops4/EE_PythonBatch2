import streamlit as st


class DashboardSOS:

    def display(self):

        st.subheader("🆘 Emergency")

        if st.button(
            "🆘 SEND SOS",
            use_container_width=True,
            type="primary"
        ):
            st.error("Emergency SOS Activated!")
            st.write("📍 Current Vehicle Location Sent")
            st.write("🚓 Emergency Services Notified")
            st.write("👨‍👩‍👧 Emergency Contact Notified")