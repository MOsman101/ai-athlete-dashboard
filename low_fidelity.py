import streamlit as st

st.set_page_config(page_title="Low-Fidelity Athlete Dashboard", layout="wide")

st.title("AI Athlete Monitoring Dashboard")
st.caption("Low-fidelity prototype: interface layout and module placement")

left, right = st.columns([1, 3])

with left:
    st.subheader("Navigation")
    st.write("Home")
    st.write("Player View")
    st.write("Performance")
    st.write("Privacy")
    st.write("Logs")

    st.subheader("Athlete Card")
    st.write("Name: Placeholder")
    st.write("Role: Midfielder")
    st.write("Status: Active")
    st.write("ID: Anonymised")

    st.subheader("Privacy Panel")
    st.write("Anonymisation: ON")
    st.write("Local Storage: ON")
    st.write("Consent Status: VERIFIED")

with right:
    a, b, c = st.columns(3)
    a.metric("Readiness", "Placeholder")
    b.metric("Training Load", "Placeholder")
    c.metric("Injury Risk", "Placeholder")

    x, y = st.columns([2, 1])
    with x:
        st.subheader("Performance Trend Area")
        st.info("Graph placeholder for workload, recovery, and readiness trends")
    with y:
        st.subheader("Model Output")
        st.info("Prediction output placeholder")
        st.info("Risk probability placeholder")

    p, q = st.columns(2)
    with p:
        st.subheader("Explainability Area")
        st.info("Placeholder for feature influence summary")
    with q:
        st.subheader("System Logs")
        st.info("Placeholder for event logging and audit traceability")