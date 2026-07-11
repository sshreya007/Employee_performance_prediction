import streamlit as st
from auth.users import authenticate
from auth.auth import login_user
from utils.session import set_page
from components.design_system import inject_css


def show():
    inject_css()

    # Extra auth-page specific overrides
    st.markdown("""
    <style>
    /* Full page dark background */
    .stApp {
      background: radial-gradient(ellipse 80% 60% at 30% 50%, rgba(124,58,237,0.18), transparent 60%),
                  radial-gradient(ellipse 50% 50% at 80% 60%, rgba(79,140,255,0.1), transparent 60%),
                  #090014 !important;
    }
    /* Card column — glass effect via container styling */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(124,58,237,0.28);
      border-radius: 20px;
      padding: 36px 32px !important;
      backdrop-filter: blur(30px);
      box-shadow: 0 0 60px rgba(124,58,237,0.1), 0 32px 64px rgba(0,0,0,0.4);
      animation: fadeInUp 0.5s ease both;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centre the card using columns
    _, col, _ = st.columns([1, 1.2, 1])

    with col:
        # ── Logo ──────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center; margin-bottom:6px;">
          <span style="font-family:'Space Grotesk',sans-serif; font-size:26px; font-weight:800;
            background:linear-gradient(135deg,#8B5CF6,#22D3EE);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            PerformaAI
          </span>
        </div>
        <div style="text-align:center; color:#334155; font-size:12px;
             letter-spacing:2px; text-transform:uppercase; margin-bottom:28px;">
          HR Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

        # ── Heading ───────────────────────────────────────────
        st.markdown("""
        <div style="margin-bottom:20px;">
          <div style="font-family:'Space Grotesk',sans-serif; font-size:22px;
               font-weight:800; color:#F1F5F9; margin-bottom:4px;">
            Welcome back 👋
          </div>
          <div style="font-size:13px; color:#475569;">
            Sign in to your HR dashboard
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Form ──────────────────────────────────────────────
        username = st.text_input("Username", placeholder="Enter your username", key="li_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass")

        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me", key="li_remember")
        with col2:
            st.markdown("""
            <div style="text-align:right; padding-top:6px;">
              <span style="color:#8B5CF6; font-size:13px; font-weight:500; cursor:pointer;">
                Forgot password?
              </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Sign in", key="login_btn", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                user = authenticate(username, password)
                if user:
                    login_user(user)
                    st.session_state["app_page"] = "home"
                    set_page("dashboard")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        # ── Divider ───────────────────────────────────────────
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin:16px 0;">
          <div style="flex:1; height:1px; background:rgba(124,58,237,0.2);"></div>
          <span style="font-size:11px; color:#334155; font-weight:500; white-space:nowrap;">
            OR CONTINUE WITH
          </span>
          <div style="flex:1; height:1px; background:rgba(124,58,237,0.2);"></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Social buttons ────────────────────────────────────
        sc1, sc2 = st.columns(2)
        with sc1:
            st.button("🔵  Google", key="google_login", use_container_width=True)
        with sc2:
            st.button("⚫  GitHub", key="github_login", use_container_width=True)

        # ── Switch to signup ──────────────────────────────────
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        ca, cb = st.columns([3, 2])
        with ca:
            st.markdown("""
            <div style="font-size:13px; color:#475569; padding-top:10px;">
              Don't have an account?
            </div>
            """, unsafe_allow_html=True)
        with cb:
            if st.button("Create account →", key="to_signup", use_container_width=True):
                set_page("signup")
                st.rerun()

        # ── Back to landing ───────────────────────────────────
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("← Back to home", key="login_home"):
            set_page("landing")
            st.rerun()

        # ── Demo hint ─────────────────────────────────────────
        st.markdown("""
        <div style="margin-top:16px; padding:12px 16px;
             background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
             border-radius:10px; font-size:12px; color:#64748B; text-align:center;">
          Demo: <code style="color:#C4B5FD;">admin</code> /
          <code style="color:#C4B5FD;">admin123</code>
          &nbsp;·&nbsp;
          <code style="color:#C4B5FD;">hrmanager</code> /
          <code style="color:#C4B5FD;">hr1234</code>
        </div>
        """, unsafe_allow_html=True)
