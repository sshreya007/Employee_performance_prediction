import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="PerformaAI — HR Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database.database import init_db
init_db()

from auth.auth import require_auth
if not require_auth():
    st.stop()

from components.topbar  import render_topbar
from components.sidebar import render_sidebar
from components.footer  import render_footer

render_topbar()
render_sidebar()

page = st.session_state.get("app_page", "home")

if page == "home":
    from home.home_view import show; show()
elif page == "prediction":
    from prediction.prediction_view import show; show()
elif page == "history":
    from history.history_view import show; show()
elif page == "profile":
    from profile.profile_view import show; show()

render_footer()