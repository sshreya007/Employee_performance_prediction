import streamlit as st
from auth.users import create_user, get_user
from auth.auth import login_user
from utils.session import set_page
from utils.validation import validate_signup

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700&display=swap');
body,.stApp{background:#090014 !important;font-family:'Inter',sans-serif;color:#fff;}
#MainMenu,footer,header,.stDeployButton{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0 !important;}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.auth-page{min-height:100vh;background:radial-gradient(ellipse 80% 60% at 70% 50%,rgba(79,140,255,.15),transparent 60%),radial-gradient(ellipse 60% 50% at 20% 60%,rgba(124,58,237,.18),transparent 60%),linear-gradient(135deg,#090014,#1A063A,#12002B);display:flex;align-items:center;justify-content:center;padding:60px 20px;}
.auth-card{background:rgba(255,255,255,.04);border:1px solid rgba(124,58,237,.3);border-radius:26px;padding:44px 40px;width:100%;max-width:440px;backdrop-filter:blur(30px);box-shadow:0 0 80px rgba(124,58,237,.12),0 40px 80px rgba(0,0,0,.5);animation:fadeInUp .6s ease both;}
.auth-logo{text-align:center;margin-bottom:6px;font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.auth-tagline{text-align:center;color:#475569;font-size:12px;margin-bottom:28px;}
.auth-title{font-size:21px;font-weight:700;margin-bottom:4px;}
.auth-sub{color:#64748B;font-size:13px;margin-bottom:22px;}
.divider{display:flex;align-items:center;gap:10px;margin:14px 0;}
.div-line{flex:1;height:1px;background:rgba(124,58,237,.2);}
.div-text{font-size:11px;color:#334155;font-weight:500;}
.social-row{display:flex;gap:10px;margin-bottom:20px;}
.btn-social{flex:1;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:10px;font-size:13px;color:#94A3B8;font-weight:600;cursor:pointer;font-family:'Inter',sans-serif;transition:all .2s;}
.btn-social:hover{background:rgba(255,255,255,.08);color:#fff;}
.auth-footer{text-align:center;font-size:13px;color:#475569;margin-top:4px;}
</style>
"""


def show():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div class="auth-page"><div class="auth-card">', unsafe_allow_html=True)

    st.markdown('<div class="auth-logo">PerformaAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-tagline">HR Intelligence Platform</div>', unsafe_allow_html=True)

    col_back, _ = st.columns([1, 3])
    with col_back:
        if st.button("← Home", key="su_home"):
            set_page("landing"); st.rerun()

    st.markdown('<div class="auth-title">Create your account ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Join your HR team on PerformaAI</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name", placeholder="Sarah Mitchell", key="su_name")
    with col2:
        username  = st.text_input("Username", placeholder="sarah_hr", key="su_user")

    email   = st.text_input("Email", placeholder="sarah@company.com", key="su_email")
    col3, col4 = st.columns(2)
    with col3:
        password = st.text_input("Password", type="password", placeholder="Min. 6 chars", key="su_pass")
    with col4:
        confirm  = st.text_input("Confirm Password", type="password", placeholder="Repeat", key="su_confirm")

    terms = st.checkbox("I accept the Terms of Service and Privacy Policy", key="su_terms")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Create Account", key="signup_btn", use_container_width=True, type="primary"):
        errors = validate_signup(full_name, username, email, password, confirm, terms)
        if get_user(username):
            errors.append("Username already taken. Please choose another.")
        if errors:
            for e in errors:
                st.error(e)
        else:
            success = create_user(full_name, username, email, password)
            if success:
                from auth.users import get_user as fetch_user
                user = fetch_user(username)
                login_user(user)
                st.session_state["app_page"] = "home"
                set_page("dashboard")
                st.rerun()
            else:
                st.error("Registration failed. Username or email may already be taken.")

    st.markdown("""
    <div class="divider"><div class="div-line"></div><div class="div-text">OR SIGN UP WITH</div><div class="div-line"></div></div>
    <div class="social-row">
      <button class="btn-social">🔵 Google</button>
      <button class="btn-social">⚫ GitHub</button>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown('<div class="auth-footer">Already have an account?</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("Login →", key="to_login"):
            set_page("login"); st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)
