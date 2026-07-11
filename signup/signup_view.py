import streamlit as st
from auth.users import create_user, get_user
from auth.auth import login_user
from utils.session import set_page
from utils.validation import validate_signup
from components.design_system import inject_css


def show():
    inject_css()

    st.markdown("""
    <style>
    .stApp {
      background: radial-gradient(ellipse 60% 50% at 70% 40%, rgba(79,140,255,0.12), transparent 60%),
                  radial-gradient(ellipse 70% 60% at 20% 70%, rgba(124,58,237,0.16), transparent 60%),
                  #090014 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.4, 1])

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
             letter-spacing:2px; text-transform:uppercase; margin-bottom:24px;">
          HR Intelligence Platform
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom:20px;">
          <div style="font-family:'Space Grotesk',sans-serif; font-size:22px;
               font-weight:800; color:#F1F5F9; margin-bottom:4px;">
            Create your account ✨
          </div>
          <div style="font-size:13px; color:#475569;">
            Join your HR team on PerformaAI
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Form ──────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full Name", placeholder="Sarah Mitchell", key="su_name")
        with c2:
            username  = st.text_input("Username",  placeholder="sarah_hr",       key="su_user")

        email = st.text_input("Email", placeholder="sarah@company.com", key="su_email")

        c3, c4 = st.columns(2)
        with c3:
            password = st.text_input("Password",         type="password", placeholder="Min. 6 chars", key="su_pass")
        with c4:
            confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat",       key="su_confirm")

        terms = st.checkbox("I accept the Terms of Service and Privacy Policy", key="su_terms")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("Create account", key="signup_btn", use_container_width=True, type="primary"):
            errors = validate_signup(full_name, username, email, password, confirm, terms)
            if get_user(username):
                errors.append("Username already taken.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                if create_user(full_name, username, email, password):
                    user = get_user(username)
                    login_user(user)
                    st.session_state["app_page"] = "home"
                    set_page("dashboard")
                    st.rerun()
                else:
                    st.error("Registration failed — email may already be in use.")

        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; margin:16px 0;">
          <div style="flex:1; height:1px; background:rgba(124,58,237,0.2);"></div>
          <span style="font-size:11px; color:#334155; font-weight:500;">OR SIGN UP WITH</span>
          <div style="flex:1; height:1px; background:rgba(124,58,237,0.2);"></div>
        </div>
        """, unsafe_allow_html=True)

        sc1, sc2 = st.columns(2)
        with sc1:
            st.button("🔵  Google", key="google_su", use_container_width=True)
        with sc2:
            st.button("⚫  GitHub", key="github_su", use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        ca, cb = st.columns([3, 2])
        with ca:
            st.markdown("""
            <div style="font-size:13px; color:#475569; padding-top:10px;">
              Already have an account?
            </div>
            """, unsafe_allow_html=True)
        with cb:
            if st.button("Sign in →", key="to_login", use_container_width=True):
                set_page("login")
                st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("← Back to home", key="su_home"):
            set_page("landing")
            st.rerun()
