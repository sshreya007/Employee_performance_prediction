import streamlit as st
from auth.users import authenticate
from auth.auth import login_user
from utils.session import set_page

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@700&display=swap');
body,.stApp{background:#090014 !important;font-family:'Inter',sans-serif;color:#fff;}
#MainMenu,footer,header,.stDeployButton{display:none !important;}
.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0 !important;}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.auth-page{min-height:100vh;background:radial-gradient(ellipse 80% 60% at 30% 50%,rgba(124,58,237,.2),transparent 60%),radial-gradient(ellipse 60% 50% at 80% 60%,rgba(79,140,255,.12),transparent 60%),linear-gradient(135deg,#090014,#12002B,#1A063A);display:flex;align-items:center;justify-content:center;padding:60px 20px;}
.auth-card{background:rgba(255,255,255,.04);border:1px solid rgba(124,58,237,.3);border-radius:26px;padding:48px 42px;width:100%;max-width:430px;backdrop-filter:blur(30px);box-shadow:0 0 80px rgba(124,58,237,.12),0 40px 80px rgba(0,0,0,.5);animation:fadeInUp .6s ease both;}
.auth-logo{text-align:center;margin-bottom:6px;font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:700;background:linear-gradient(135deg,#8B5CF6,#22D3EE);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.auth-tagline{text-align:center;color:#475569;font-size:12px;margin-bottom:32px;}
.auth-title{font-size:22px;font-weight:700;margin-bottom:4px;}
.auth-sub{color:#64748B;font-size:13px;margin-bottom:24px;}
.divider{display:flex;align-items:center;gap:10px;margin:16px 0;}
.div-line{flex:1;height:1px;background:rgba(124,58,237,.2);}
.div-text{font-size:11px;color:#334155;font-weight:500;}
.social-row{display:flex;gap:10px;margin-bottom:24px;}
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
        if st.button("← Home", key="login_home"):
            set_page("landing"); st.rerun()

    st.markdown('<div class="auth-title">Welcome back 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Sign in to your HR dashboard</div>', unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username", key="li_user")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="li_pass")

    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Remember me", key="li_remember")
    with col2:
        st.markdown('<div style="text-align:right;padding-top:4px;"><a style="color:#8B5CF6;font-size:13px;text-decoration:none;font-weight:500;" href="#">Forgot password?</a></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔐 Login", key="login_btn", use_container_width=True, type="primary"):
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
                st.error("❌ Invalid username or password.")

    st.markdown("""
    <div class="divider"><div class="div-line"></div><div class="div-text">OR CONTINUE WITH</div><div class="div-line"></div></div>
    <div class="social-row">
      <button class="btn-social">🔵 Google</button>
      <button class="btn-social">⚫ GitHub</button>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown('<div class="auth-footer">Don\'t have an account?</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("Sign Up →", key="to_signup"):
            set_page("signup"); st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)
