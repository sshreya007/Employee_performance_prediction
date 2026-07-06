"""
app.py — PerformaAI Main Entry Point
======================================
Run:   streamlit run app.py

Auth flow:
  Landing  →  Login / Sign Up  →  Dashboard
  Dashboard routes:  Home · Prediction · History · Profile
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

# ── 1. Page config (must be first Streamlit call) ───────────
st.set_page_config(
    page_title="PerformaAI — HR Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. Init database on first run ───────────────────────────
from database.database import init_db
init_db()

# ── 3. Auth gate ────────────────────────────────────────────
from auth.auth import require_auth
if not require_auth():
    st.stop()

# ════════════════════════════════════════════════════════════
#  User is authenticated — render the dashboard
# ════════════════════════════════════════════════════════════
from components.topbar  import render_topbar
from components.sidebar import render_sidebar
from components.footer  import render_footer

render_topbar()
render_sidebar()

# ── Route to active feature ─────────────────────────────────
page = st.session_state.get("app_page", "home")

if page == "home":
    from home.home_view import show
    show()

elif page == "prediction":
    # placeholder until next response
    from components.design_system import inject_css
    inject_css()
    st.markdown('<div class="page-wrap"><div class="page-title">🔮 Prediction — Coming Soon</div></div>',
                unsafe_allow_html=True)

elif page == "history":
    from components.design_system import inject_css
    inject_css()
    st.markdown('<div class="page-wrap"><div class="page-title">📋 History — Coming Soon</div></div>',
                unsafe_allow_html=True)

elif page == "profile":
    from components.design_system import inject_css
    inject_css()
    st.markdown('<div class="page-wrap"><div class="page-title">👤 Profile — Coming Soon</div></div>',
                unsafe_allow_html=True)

render_footer()
