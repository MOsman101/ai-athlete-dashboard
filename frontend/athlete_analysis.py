import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from backend.logs import add_log
from backend.data_loader import get_athlete_list, get_athlete_history, get_latest_athlete_record
from backend.preprocess import prepare_single_input
from backend.model import predict_risk, get_feature_importance
from backend.scoring import calculate_readiness_score, generate_performance_summary
from backend.privacy import anonymise_athlete_id


def apply_chart_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=15),
        title_font=dict(color="#ffffff", size=20),
        legend=dict(font=dict(color="#ffffff", size=13)),
        xaxis=dict(
            title_font=dict(color="#ffffff", size=14),
            tickfont=dict(color="#ffffff", size=12),
            gridcolor="rgba(255,255,255,0.22)"
        ),
        yaxis=dict(
            title_font=dict(color="#ffffff", size=14),
            tickfont=dict(color="#ffffff", size=12),
            gridcolor="rgba(255,255,255,0.22)"
        )
    )
    return fig


def render_athlete_analysis(df, model, logs_list):
    athlete_list = get_athlete_list(df)
    selected_athlete = st.selectbox("Select Athlete ID", athlete_list)

    athlete_history = get_athlete_history(df, selected_athlete)
    latest_record = get_latest_athlete_record(df, selected_athlete)

    profile, controls = st.columns([1, 2.2])

    with profile:
        initials = str(latest_record["athlete_name"]).replace("Player ", "P")
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="avatar-box">{initials}</div>
                <div class="profile-name">{latest_record['athlete_name']}</div>
                <div class="profile-meta">{latest_record['position']} · {latest_record['club']}</div>
                <div class="info-row"><span class="info-label">Athlete ID</span><span class="info-value">{anonymise_athlete_id(selected_athlete)}</span></div>
                <div class="info-row"><span class="info-label">Age</span><span class="info-value">{latest_record['age']}</span></div>
                <div class="info-row"><span class="info-label">Previous Injury</span><span class="info-value">{latest_record['previous_injury_flag']}</span></div>
                <div class="info-row"><span class="info-label">Storage</span><span class="info-value">Local / Cloud DB</span></div>
                <div class="info-row"><span class="info-label">Consent</span><span class="info-value">Verified</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with controls:
        col1, col2, col3 = st.columns(3)

        with col1:
            heart_rate = st.slider("Heart Rate", 45, 110, int(latest_record["heart_rate"]))
            hrv = st.slider("HRV", 20, 100, int(latest_record["hrv"]))
            training_load = st.slider("Training Load", 20, 120, int(latest_record["training_load"]))

        with col2:
            fatigue_score = st.slider("Fatigue Score", 1, 10, int(latest_record["fatigue_score"]))
            recovery_hours = st.slider("Recovery Hours", 3, 12, int(latest_record["recovery_hours"]))
            sleep_hours = st.slider("Sleep Hours", 3, 10, int(latest_record["sleep_hours"]))

        with col3:
            previous_injury = st.selectbox(
                "Previous Injury Flag",
                [0, 1],
                index=int(latest_record["previous_injury_flag"])
            )

        input_df = prepare_single_input(
            heart_rate,
            hrv,
            training_load,
            fatigue_score,
            recovery_hours,
            sleep_hours,
            previous_injury
        )

        prediction, probabilities = predict_risk(model, input_df)

        readiness_score = calculate_readiness_score(
            heart_rate,
            hrv,
            training_load,
            fatigue_score,
            recovery_hours,
            sleep_hours
        )

        injury_risk = "High" if prediction == 1 else "Low"
        risk_probability = f"{probabilities[1]:.2%}"

        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Injury Risk", injury_risk)
        m2.metric("Risk Probability", risk_probability)
        m3.metric("Readiness Score", f"{readiness_score}")

        if st.button("Log Prediction Event"):
            add_log(
                logs_list,
                "Prediction generated",
                "Success",
                f"{selected_athlete} assessed with risk={injury_risk} and readiness={readiness_score}"
            )
            st.success("Prediction event logged successfully.")

    lower_left, lower_right = st.columns(2)

    with lower_left:
        feature_df = get_feature_importance(model)
        fig_bar = px.bar(
            feature_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )
        fig_bar = apply_chart_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)

    with lower_right:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=readiness_score,
            title={"text": "Readiness Gauge", "font": {"color": "#ffffff", "size": 20}},
            number={"font": {"color": "#ffffff", "size": 56}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickcolor": "#ffffff",
                    "tickfont": {"color": "#ffffff"}
                },
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 40], "color": "#dc2626"},
                    {"range": [40, 70], "color": "#facc15"},
                    {"range": [70, 100], "color": "#22c55e"}
                ]
            }
        ))
        gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=15)
        )
        st.plotly_chart(gauge, use_container_width=True)

        st.info(generate_performance_summary(training_load, fatigue_score, recovery_hours))

    fig_trend = px.line(
        athlete_history,
        x="session_date",
        y=["training_load", "recovery_hours", "readiness_score"],
        title=f"Session History for {selected_athlete}"
    )
    fig_trend = apply_chart_theme(fig_trend)
    st.plotly_chart(fig_trend, use_container_width=True)