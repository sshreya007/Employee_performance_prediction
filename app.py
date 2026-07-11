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
    from components.design_system import inject_css
    inject_css()
    st.markdown('<div style="padding:28px 36px;"><div style="font-family:Space Grotesk,sans-serif;font-size:28px;font-weight:800;color:#F1F5F9;">📋 History — Coming Soon</div></div>', unsafe_allow_html=True)

elif page == "profile":
    from components.design_system import inject_css
    inject_css()
    st.markdown('<div style="padding:28px 36px;"><div style="font-family:Space Grotesk,sans-serif;font-size:28px;font-weight:800;color:#F1F5F9;">👤 Profile — Coming Soon</div></div>', unsafe_allow_html=True)

render_footer()