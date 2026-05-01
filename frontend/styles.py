import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-image:
                linear-gradient(rgba(5, 12, 28, 0.58), rgba(5, 12, 28, 0.72)),
                url("https://images.unsplash.com/photo-1518091043644-c1d4457512c6?auto=format&fit=crop&w=2200&q=80");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #f8fafc !important;
        }

        header[data-testid="stHeader"] {
            background: rgba(0,0,0,0) !important;
            height: 0rem;
        }

        div[data-testid="stDecoration"] {
            display: none;
        }

        .block-container {
            padding-top: 0rem;
            padding-bottom: 2rem;
            max-width: 1600px;
        }

        section[data-testid="stSidebar"] {
            background: rgba(3, 7, 18, 0.9);
            border-right: 1px solid rgba(255,255,255,0.16);
            backdrop-filter: blur(10px);
        }

        section[data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }

        .main-title {
            font-size: 3.6rem;
            font-weight: 900;
            color: #ffffff !important;
            margin-bottom: 0.4rem;
            text-shadow: 0 3px 12px rgba(0,0,0,0.75);
        }

        .main-subtitle {
            color: #e2e8f0 !important;
            font-size: 1.35rem;
            margin-bottom: 0rem;
            text-shadow: 0 2px 8px rgba(0,0,0,0.65);
        }

        .hero-panel {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 28px;
            padding: 40px 50px;
            margin-bottom: 26px;
            box-shadow: 0 18px 44px rgba(0,0,0,0.38);
            backdrop-filter: blur(9px);
        }

        .dashboard-card {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 14px 34px rgba(0,0,0,0.34);
            margin-bottom: 20px;
            backdrop-filter: blur(9px);
            color: #f8fafc !important;
        }

        .profile-card {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 26px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 14px 34px rgba(0,0,0,0.38);
            backdrop-filter: blur(9px);
            color: #f8fafc !important;
        }

        .avatar-box {
            width: 160px;
            height: 200px;
            margin: 0 auto 18px auto;
            background: linear-gradient(180deg, #e5e7eb, #94a3b8);
            border-radius: 20px;
            border: 4px solid rgba(255,255,255,0.92);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3.7rem;
            font-weight: 900;
            color: #0f172a !important;
        }

        .profile-name {
            font-size: 1.65rem;
            font-weight: 900;
            margin-bottom: 6px;
            color: #ffffff !important;
        }

        .profile-meta {
            color: #dbeafe !important;
            font-size: 1.12rem;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255,255,255,0.15);
            padding: 9px 0;
            font-size: 1.08rem;
        }

        .info-label {
            color: #cbd5e1 !important;
            font-weight: 500;
        }

        .info-value {
            color: #ffffff !important;
            font-weight: 800;
        }

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(255,255,255,0.18);
            padding: 22px;
            border-radius: 22px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.30);
            color: #f8fafc !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #dbeafe !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-size: 2.1rem !important;
            font-weight: 900 !important;
        }

        .stButton>button {
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.28);
            background: linear-gradient(90deg, #16a34a, #2563eb);
            color: white !important;
            font-weight: 800;
            font-size: 1.1rem;
            padding: 0.8rem 1.2rem;
        }

        .stButton>button:hover {
            border: 1px solid white;
            color: white !important;
        }

        html, body, [class*="css"] {
            color: #f8fafc !important;
        }

        .stMarkdown, .stText, .stCaption {
            color: #f8fafc !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 800 !important;
        }

        p, label, span {
            color: #e2e8f0 !important;
            font-size: 1.08rem;
        }

        input {
            font-size: 1.15rem !important;
            padding: 10px !important;
        }

        .stSelectbox label,
        .stSlider label,
        .stTextInput label,
        .stRadio label {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        .js-plotly-plot .plotly text {
            fill: #ffffff !important;
        }

        .js-plotly-plot .gtitle,
        .js-plotly-plot .xtitle,
        .js-plotly-plot .ytitle {
            fill: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )