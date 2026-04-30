import streamlit as st
from backend.logs import get_logs_dataframe


def render_system_logs(logs_list):
    st.subheader("System Logs")

    logs_df = get_logs_dataframe(logs_list)
    st.dataframe(logs_df, use_container_width=True)

    st.info(
        "The logs panel demonstrates traceability and accountability within the prototype. "
        "It records key dashboard actions and system events during the active session."
    )