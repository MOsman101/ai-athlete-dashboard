import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from backend.data_loader import get_latest_records_for_all_athletes
from backend.privacy import get_privacy_status


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


def render_overview(df, accuracy, logs_list):
    latest_df = get_latest_records_for_all_athletes(df)
    selected = latest_df.iloc[0]
    privacy_status = get_privacy_status()

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Model Accuracy", f"{accuracy:.2%}")
    top2.metric("Readiness Score", f"{selected['readiness_score']}")
    top3.metric("Training Load", f"{selected['training_load']:.1f}")
    top4.metric("Injury Risk", "High" if selected["injury_risk"] == 1 else "Low")

    left, right = st.columns([1, 3])

    with left:
        initials = str(selected["athlete_name"]).replace("Player ", "P")
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="avatar-box">{initials}</div>
                <div class="profile-name">{selected['athlete_name']}</div>
                <div class="profile-meta">{selected['position']} · {selected['club']}</div>
                <div class="info-row"><span class="info-label">Athlete ID</span><span class="info-value">{selected['athlete_id']}</span></div>
                <div class="info-row"><span class="info-label">Age</span><span class="info-value">{selected['age']}</span></div>
                <div class="info-row"><span class="info-label">Heart Rate</span><span class="info-value">{selected['heart_rate']}</span></div>
                <div class="info-row"><span class="info-label">HRV</span><span class="info-value">{selected['hrv']}</span></div>
                <div class="info-row"><span class="info-label">Recovery</span><span class="info-value">{selected['recovery_hours']} hrs</span></div>
                <div class="info-row"><span class="info-label">Storage</span><span class="info-value">{privacy_status['storage']}</span></div>
                <div class="info-row"><span class="info-label">Consent</span><span class="info-value">{privacy_status['consent']}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        athlete_history = df[df["athlete_id"] == selected["athlete_id"]].sort_values("session_date")

        fig_line = px.line(
            athlete_history,
            x="session_date",
            y=["training_load", "recovery_hours", "readiness_score"],
            title="Performance Trend Overview"
        )
        fig_line = apply_chart_theme(fig_line)
        st.plotly_chart(fig_line, use_container_width=True)

        bottom_left, bottom_right = st.columns(2)

        with bottom_left:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=float(selected["readiness_score"]),
                title={"text": "Athlete Readiness", "font": {"color": "#ffffff", "size": 20}},
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

        with bottom_right:
            risk_counts = latest_df["injury_risk"].value_counts().rename(index={0: "Low Risk", 1: "High Risk"})
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Distribution"
            )
            fig_pie = apply_chart_theme(fig_pie)
            fig_pie.update_traces(textfont=dict(color="#ffffff", size=14))
            st.plotly_chart(fig_pie, use_container_width=True)