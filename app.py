import streamlit as st
from frontend.styles import apply_global_styles
from frontend.overview import render_overview
from frontend.athlete_analysis import render_athlete_analysis
from frontend.privacy import render_privacy
from frontend.system_logs import render_system_logs
from backend.logs import initialise_logs, add_log
from backend.data_loader import load_dataset
from backend.model import train_model
from backend.auth import verify_login, register_user, get_accessible_pages

st.set_page_config(
    page_title="Rush",
    page_icon="⚽",
    layout="wide"
)

apply_global_styles()

if "system_logs" not in st.session_state:
    st.session_state.system_logs = initialise_logs()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None


@st.cache_data
def get_dataset():
    return load_dataset()


@st.cache_resource
def get_trained_model(df):
    return train_model(df)


def logout():
    add_log(
        st.session_state.system_logs,
        "User logged out",
        "Success",
        f"{st.session_state.username} logged out"
    )
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.user_role = None


if not st.session_state.authenticated:
    st.markdown(
        """
        <div class="hero-panel">
            <div class="rush-brand">
                <div class="rush-logo">R</div>
                <div class="rush-title-block">
                    <div class="rush-wordmark">Rush</div>
                    <div class="rush-tagline">Secure privacy-aware performance analytics platform</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, centre, right = st.columns([1, 1.4, 1])

    with centre:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)

        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            st.markdown("## Login to Rush")

            username = st.text_input(
                "Username",
                placeholder="Enter username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password"
            )

            if st.button("Login", use_container_width=True, key="login_button"):
                valid, role = verify_login(username, password)

                if valid:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = role

                    add_log(
                        st.session_state.system_logs,
                        "User logged in",
                        "Success",
                        f"{username} logged in as {role}"
                    )

                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with register_tab:
            st.markdown("## Create Viewer Account")
            st.caption("New accounts are automatically assigned Viewer access.")

            new_username = st.text_input(
                "New Username",
                placeholder="Create a username",
                key="register_username"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Create a password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm password",
                key="confirm_password"
            )

            if st.button("Register", use_container_width=True, key="register_button"):
                if new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_password)

                    if success:
                        add_log(
                            st.session_state.system_logs,
                            "New user registered",
                            "Success",
                            f"{new_username} registered as Viewer"
                        )
                        st.success(message)
                    else:
                        st.error(message)

        st.markdown('</div>', unsafe_allow_html=True)

else:
    df = get_dataset()
    model, accuracy = get_trained_model(df)
    accessible_pages = get_accessible_pages(st.session_state.user_role)

    st.markdown(
        """
        <div class="hero-panel">
            <div class="rush-brand">
                <div class="rush-logo">R</div>
                <div class="rush-title-block">
                    <div class="rush-wordmark">Rush</div>
                    <div class="rush-tagline">Balancing performance analytics with privacy-aware design</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("## Rush")
    st.sidebar.markdown(f"**User:** {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")

    if st.sidebar.button("Logout", use_container_width=True):
        logout()
        st.rerun()

    st.sidebar.markdown("---")

    selected_page = st.sidebar.radio(
        "Navigation",
        accessible_pages
    )

    st.sidebar.markdown("---")
    st.sidebar.success("Online deployment ready")
    st.sidebar.info("Synthetic athlete dataset")
    st.sidebar.warning("Privacy-aware prototype")

    if selected_page == "Executive Overview":
        add_log(
            st.session_state.system_logs,
            "Executive Overview opened",
            "Success",
            f"{st.session_state.username} accessed overview"
        )
        render_overview(df, accuracy, st.session_state.system_logs)

    elif selected_page == "Athlete Analysis":
        add_log(
            st.session_state.system_logs,
            "Athlete Analysis opened",
            "Success",
            f"{st.session_state.username} accessed athlete analysis"
        )
        render_athlete_analysis(df, model, st.session_state.system_logs)

    elif selected_page == "Privacy":
        add_log(
            st.session_state.system_logs,
            "Privacy opened",
            "Success",
            f"{st.session_state.username} accessed privacy page"
        )
        render_privacy(st.session_state.user_role, st.session_state.system_logs)

    elif selected_page == "System Logs":
        add_log(
            st.session_state.system_logs,
            "System Logs opened",
            "Success",
            f"{st.session_state.username} accessed logs page"
        )
        render_system_logs(st.session_state.system_logs)