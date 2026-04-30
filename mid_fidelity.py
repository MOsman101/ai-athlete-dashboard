import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Mid-Fidelity Athlete Dashboard", layout="wide")

st.title("AI Athlete Monitoring Dashboard")
st.caption("Mid-fidelity prototype: functional interface with synthetic athlete information and dashboard outputs")

np.random.seed(42)

timeline = pd.DataFrame({
    "Session": list(range(1, 11)),
    "Training Load": np.random.randint(55, 95, 10),
    "Recovery": np.random.randint(60, 95, 10),
    "Readiness": np.random.randint(58, 93, 10)
})

metrics_df = pd.DataFrame({
    "Metric": ["Fatigue", "Load", "Recovery", "Sleep"],
    "Value": [65, 74, 79, 81]
})

distribution_df = pd.DataFrame({
    "Category": ["Low Risk", "Moderate Risk", "High Risk"],
    "Value": [14, 9, 3]
})

left, right = st.columns([1, 3])

with left:
    st.subheader("Player Profile")
    st.write("Name: Jamal M.")
    st.write("Position: Attacking Midfielder")
    st.write("Age: 21")
    st.write("Match Status: Available")
    st.write("Profile ID: AM-014")

    st.subheader("Privacy Status")
    st.write("Anonymisation: Enabled")
    st.write("Local Storage: Enabled")
    st.write("Consent Status: Verified")
    st.write("Data Source: Synthetic")

    st.subheader("Navigation")
    st.write("Dashboard Overview")
    st.write("Athlete Metrics")
    st.write("Recovery Trends")
    st.write("Privacy Controls")
    st.write("System Logs")

with right:
    a, b, c, d = st.columns(4)
    a.metric("Readiness Score", "82")
    b.metric("Training Load", "74")
    c.metric("Recovery Score", "79")
    d.metric("Injury Risk", "Moderate")

    upper_left, upper_right = st.columns([2, 1])

    with upper_left:
        st.subheader("Athlete Performance Trends")
        fig_trend = px.line(
            timeline,
            x="Session",
            y=["Training Load", "Recovery", "Readiness"],
            title="Performance Trend Overview"
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with upper_right:
        st.subheader("Performance Summary")
        st.info(
            "Current fatigue level is moderate. Recovery trend remains stable. "
            "Training load has increased slightly across recent sessions. "
            "Additional monitoring is advisable before the next match cycle."
        )

        st.subheader("Risk Distribution")
        fig_distribution = px.pie(
            distribution_df,
            names="Category",
            values="Value",
            title="Risk Distribution"
        )
        st.plotly_chart(fig_distribution, use_container_width=True)

    lower_left, lower_right = st.columns(2)

    with lower_left:
        st.subheader("Current Monitoring Metrics")
        fig_bar = px.bar(
            metrics_df,
            x="Metric",
            y="Value",
            title="Monitoring Metrics"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with lower_right:
        st.subheader("Explainability Panel")
        st.info(
            "Most influential variables in the current monitoring logic:\n"
            "- Training load\n"
            "- Recovery score\n"
            "- Fatigue state\n"
            "- Sleep quality"
        )

        st.subheader("System Output")
        st.success(
            "Based on the current pattern of synthetic data, the athlete remains in a stable state, "
            "although rising workload may increase future injury probability if recovery declines."
        )

        st.subheader("System Logs")
        logs_df = pd.DataFrame({
            "Time": ["09:00", "09:01", "09:02", "09:03"],
            "Event": [
                "Dataset loaded",
                "Dashboard session started",
                "Monitoring metrics rendered",
                "Summary output generated"
            ]
        })
        st.dataframe(logs_df, use_container_width=True)