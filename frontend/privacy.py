import streamlit as st
import pandas as pd
from backend.privacy import get_privacy_status, get_access_matrix


def render_privacy(user_role, logs_list):
    st.subheader("Privacy")

    privacy_status = get_privacy_status()

    c1, c2, c3 = st.columns(3)
    c1.metric("Anonymisation", privacy_status["anonymisation"])
    c2.metric("Storage", privacy_status["storage"])
    c3.metric("Consent Layer", privacy_status["consent"])

    st.markdown("### Privacy Controls")
    st.write("- Synthetic data only: no real athlete data is collected or processed.")
    st.write("- Athlete records are represented using anonymised IDs.")
    st.write("- Dashboard runs locally and avoids third-party data transmission.")
    st.write("- Only essential variables are processed to support data minimisation.")
    st.write("- Access is controlled through role-based permissions.")

    st.markdown("### Current Role")
    st.info(f"Logged in as: {user_role}")

    st.markdown("### Access Levels")
    access_df = pd.DataFrame(get_access_matrix())
    st.dataframe(access_df, use_container_width=True)