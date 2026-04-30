import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #071a3d 0%, #0b3d91 45%, #111827 100%);
            color: white;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #061735 0%, #0b3d91 100%);
            border-right: 1px solid rgba(255,255,255,0.15);
        }

        section[data-testid="stSidebar"] * {
            color: white;
        }

        .block-container {
            padding-top: 1.5rem;
            max-width: 1450px;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: white;
            margin-bottom: 0.2rem;
        }

        .main-subtitle {
            color: #cbd5e1;
            font-size: 1rem;
            margin-bottom: 1.2rem;
        }

        .dashboard-card {
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.28);
            margin-bottom: 18px;
        }

        .profile-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.16), rgba(255,255,255,0.08));
            border: 1px solid rgba(255,255,255,0.22);
            border-radius: 24px;
            padding: 22px;
            text-align: center;
            box-shadow: 0 12px 28px rgba(0,0,0,0.3);
        }

        .avatar-box {
            width: 135px;
            height: 165px;
            margin: 0 auto 16px auto;
            background: linear-gradient(180deg, #e5e7eb, #94a3b8);
            border-radius: 18px;
            border: 4px solid rgba(255,255,255,0.85);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            font-weight: 900;
            color: #0f172a;
        }

        .profile-name {
            font-size: 1.35rem;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .profile-meta {
            color: #dbeafe;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            padding: 7px 0;
            font-size: 0.95rem;
        }

        .info-label {
            color: #cbd5e1;
        }

        .info-value {
            color: white;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            padding: 14px;
            border-radius: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }

        div[data-testid="stMetric"] label {
            color: #dbeafe !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: white !important;
        }

        .stButton>button {
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.25);
            background: linear-gradient(90deg, #2563eb, #dc2626);
            color: white;
            font-weight: 700;
            padding: 0.6rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )