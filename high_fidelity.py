import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="High-Fidelity Athlete Dashboard", layout="wide")

st.title("AI Athlete Monitoring Dashboard")
st.caption("High-fidelity prototype: privacy-aware predictive analytics dashboard for elite sport")

@st.cache_data
def generate_data(n=300, seed=42):
    np.random.seed(seed)

    df = pd.DataFrame({
        "athlete_id": [f"Athlete_{i:03d}" for i in range(1, n + 1)],
        "heart_rate": np.random.normal(72, 8, n).clip(45, 110),
        "hrv": np.random.normal(58, 10, n).clip(20, 100),
        "training_load": np.random.normal(70, 15, n).clip(20, 120),
        "fatigue_score": np.random.normal(5, 2, n).clip(1, 10),
        "recovery_hours": np.random.normal(8, 1.5, n).clip(3, 12),
        "sleep_hours": np.random.normal(7.2, 1.2, n).clip(3, 10),
        "previous_injury_flag": np.random.binomial(1, 0.28, n)
    })

    risk_formula = (
        (df["training_load"] * 0.03)
        + (df["fatigue_score"] * 0.9)
        - (df["recovery_hours"] * 0.5)
        - (df["sleep_hours"] * 0.35)
        - (df["hrv"] * 0.02)
        + (df["previous_injury_flag"] * 1.0)
    )

    df["injury_risk"] = np.where(risk_formula > 4.8, 1, 0)

    readiness = (
        100
        - (df["fatigue_score"] * 6)
        - (df["training_load"] * 0.25)
        + (df["recovery_hours"] * 4)
        + (df["sleep_hours"] * 2.5)
        + (df["hrv"] * 0.15)
    )

    df["readiness_score"] = readiness.clip(0, 100).round(1)

    return df

df = generate_data()

features = [
    "heart_rate",
    "hrv",
    "training_load",
    "fatigue_score",
    "recovery_hours",
    "sleep_hours",
    "previous_injury_flag"
]

X = df[features]
y = df["injury_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

st.sidebar.header("Dashboard Navigation")
page = st.sidebar.radio(
    "Select section",
    ["Executive Overview", "Athlete Analysis", "Privacy and Ethics", "System Logs"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
st.sidebar.success("Local deployment")
st.sidebar.info("Synthetic data only")
st.sidebar.warning("Research prototype")

if page == "Executive Overview":
    selected = df.iloc[16]

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Model Accuracy", f"{accuracy:.2%}")
    top2.metric("Readiness Score", f"{selected['readiness_score']}")
    top3.metric("Training Load", f"{selected['training_load']:.0f}")
    top4.metric("Injury Risk", "High" if selected["injury_risk"] == 1 else "Low")

    left, right = st.columns([1, 3])

    with left:
        st.subheader("Player Profile")
        st.write("Name: Kingsley K.")
        st.write("Position: Winger")
        st.write("Age: 27")
        st.write("Status: Match Fit")
        st.write("Profile ID: WK-017")
        st.write("Data Type: Synthetic")

        st.subheader("Privacy Controls")
        st.write("Anonymisation: Enabled")
        st.write("Local Storage: Active")
        st.write("Consent Layer: Verified")
        st.write("Data Minimisation: Applied")

    with right:
        trend_df = df.head(40).copy()
        trend_df["Session"] = range(1, 41)

        fig_line = px.line(
            trend_df,
            x="Session",
            y=["training_load", "readiness_score", "recovery_hours"],
            title="Performance Trend Overview"
        )
        st.plotly_chart(fig_line, use_container_width=True)

        bottom_left, bottom_right = st.columns([1, 1])

        with bottom_left:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(selected["readiness_score"]),
                title={"text": "Athlete Readiness"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "steps": [
                        {"range": [0, 40], "color": "lightcoral"},
                        {"range": [40, 70], "color": "khaki"},
                        {"range": [70, 100], "color": "lightgreen"}
                    ]
                }
            ))
            st.plotly_chart(gauge, use_container_width=True)

        with bottom_right:
            risk_counts = df["injury_risk"].value_counts().rename(index={0: "Low Risk", 1: "High Risk"})
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

elif page == "Athlete Analysis":
    athlete = st.selectbox("Select athlete", df["athlete_id"].tolist())
    athlete_row = df[df["athlete_id"] == athlete].iloc[0]

    input_col1, input_col2, input_col3 = st.columns(3)

    with input_col1:
        heart_rate = st.slider("Heart Rate", 45, 110, int(athlete_row["heart_rate"]))
        hrv = st.slider("HRV", 20, 100, int(athlete_row["hrv"]))
        training_load = st.slider("Training Load", 20, 120, int(athlete_row["training_load"]))

    with input_col2:
        fatigue_score = st.slider("Fatigue Score", 1, 10, int(athlete_row["fatigue_score"]))
        recovery_hours = st.slider("Recovery Hours", 3, 12, int(athlete_row["recovery_hours"]))
        sleep_hours = st.slider("Sleep Hours", 3, 10, int(athlete_row["sleep_hours"]))

    with input_col3:
        previous_injury_flag = st.selectbox("Previous Injury Flag", [0, 1], int(athlete_row["previous_injury_flag"]))
        st.write(f"Anonymised ID: {athlete.replace('Athlete_', 'ID-')}")
        st.write("Storage Mode: Local")
        st.write("Data Source: Synthetic")

    input_data = pd.DataFrame([{
        "heart_rate": heart_rate,
        "hrv": hrv,
        "training_load": training_load,
        "fatigue_score": fatigue_score,
        "recovery_hours": recovery_hours,
        "sleep_hours": sleep_hours,
        "previous_injury_flag": previous_injury_flag
    }])

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    readiness_score = (
        100
        - (fatigue_score * 6)
        - (training_load * 0.25)
        + (recovery_hours * 4)
        + (sleep_hours * 2.5)
        + (hrv * 0.15)
    )
    readiness_score = max(0, min(100, round(readiness_score, 1)))

    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Injury Risk", "High" if prediction == 1 else "Low")
    m2.metric("Risk Probability", f"{probabilities[1]:.2%}")
    m3.metric("Readiness Score", f"{readiness_score}")

    lower_left, lower_right = st.columns([1, 1])

    with lower_left:
        fig_bar = px.bar(
            feature_importance,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Model Feature Importance"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with lower_right:
        st.subheader("Explainability Summary")
        st.info(
            "The strongest contributing variables in the current model are training load, "
            "fatigue score, recovery hours, and heart rate variability. This improves "
            "interpretability by showing which features most influence the output."
        )

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=readiness_score,
            title={"text": "Readiness Gauge"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "lightcoral"},
                    {"range": [40, 70], "color": "khaki"},
                    {"range": [70, 100], "color": "lightgreen"}
                ]
            }
        ))
        st.plotly_chart(gauge, use_container_width=True)

elif page == "Privacy and Ethics":
    st.subheader("Privacy-by-Design Implementation")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Anonymisation", "Enabled")
    with c2:
        st.metric("Storage", "Local Only")
    with c3:
        st.metric("Consent Layer", "Verified")

    st.markdown("### Ethical Design Indicators")
    st.write("- Synthetic data only: no real athlete data is collected or processed.")
    st.write("- Anonymised identifiers are used in place of personal names.")
    st.write("- Local deployment reduces third-party data exposure.")
    st.write("- Restricted variables support data minimisation.")
    st.write("- Explainability output reduces black-box decision opacity.")

    ethics_df = pd.DataFrame({
        "Principle": [
            "Privacy-by-design",
            "Transparency",
            "Data minimisation",
            "Autonomy support",
            "Responsible AI"
        ],
        "Implementation in Prototype": [
            "Local storage and anonymised records",
            "Feature importance chart and visible privacy panel",
            "Only essential synthetic inputs are processed",
            "Consent and privacy indicators shown in the interface",
            "Prediction and ethics integrated into one dashboard"
        ]
    })

    st.dataframe(ethics_df, use_container_width=True)

elif page == "System Logs":
    st.subheader("System Logs and Traceability")

    logs_df = pd.DataFrame({
        "Time": ["09:00", "09:01", "09:02", "09:03", "09:05", "09:06"],
        "Event": [
            "Synthetic dataset loaded",
            "Dashboard session started",
            "Prediction engine initialised",
            "Athlete analysis opened",
            "Privacy panel checked",
            "Dashboard refreshed"
        ],
        "Status": ["Success", "Success", "Success", "Success", "Success", "Success"]
    })

    st.dataframe(logs_df, use_container_width=True)

    st.info(
        "The log panel demonstrates traceability and accountability within the prototype, "
        "supporting the ethical and technical rationale of the system."
    )