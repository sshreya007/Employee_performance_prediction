import streamlit as st
from auth.auth import logout

NAV = [
    ("🏠", "Home",       "home"),
    ("🔮", "Prediction", "prediction"),
    ("📋", "History",    "history"),
    ("👤", "Profile",    "profile"),
]


def render_sidebar():
    with st.sidebar:
        # Extra sidebar-specific CSS
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
          background: #0D001F !important;
          border-right: 1px solid rgba(124,58,237,0.15) !important;
        }
        section[data-testid="stSidebar"] > div:first-child {
          padding: 0 !important;
        }
        /* Kill ALL default button styling in sidebar */
        section[data-testid="stSidebar"] .stButton > button {
          all: unset !important;
          display: block !important;
          width: 100% !important;
          padding: 10px 16px !important;
          font-size: 14px !important;
          font-weight: 500 !important;
          color: #64748B !important;
          border-radius: 10px !important;
          cursor: pointer !important;
          transition: background 0.2s, color 0.2s !important;
          margin: 1px 0 !important;
          font-family: 'Inter', sans-serif !important;
          box-shadow: none !important;
          border: none !important;
          background: transparent !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
          background: rgba(124,58,237,0.12) !important;
          color: #C4B5FD !important;
        }
        /* Remove stButton wrapper margins */
        section[data-testid="stSidebar"] .stButton {
          margin: 4px 0 !important;
          padding: 0 8px !important;
        }
        /* Divider */
        section[data-testid="stSidebar"] hr {
          margin: 10px 16px !important;
          border: none !important;
          height: 1px !important;
          background: rgba(124,58,237,0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # ── Logo ──────────────────────────────────────────────
        st.markdown("""
        <div style="padding:24px 20px 10px; text-align:center;">
          <div style="font-family:'Space Grotesk',sans-serif; font-size:20px; font-weight:800;
               background:linear-gradient(135deg,#8B5CF6,#22D3EE);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            PerformaAI
          </div>
          <div style="font-size:9px; color:#1E293B; letter-spacing:3px;
               text-transform:uppercase; font-weight:700; margin-top:2px;">
            HR Intelligence
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── User card ─────────────────────────────────────────
        name       = st.session_state.get("name", "User")
        role       = st.session_state.get("role", "hr")
        initial    = name[0].upper() if name else "U"
        role_color = "#7C3AED" if role == "admin" else "#22D3EE"

        st.markdown(f"""
        <div style="margin:8px 12px 14px; padding:14px 12px;
             background:linear-gradient(135deg,rgba(124,58,237,0.1),rgba(34,211,238,0.05));
             border:1px solid rgba(124,58,237,0.22); border-radius:14px; text-align:center;">
          <div style="width:40px; height:40px; border-radius:50%; margin:0 auto 8px;
               background:linear-gradient(135deg,#7C3AED,#22D3EE);
               display:flex; align-items:center; justify-content:center;
               font-size:16px; font-weight:800; color:#fff;
               box-shadow:0 0 16px rgba(124,58,237,0.35);">
            {initial}
          </div>
          <div style="font-weight:700; font-size:13px; color:#E2E8F0; margin-bottom:6px;">
            {name}
          </div>
          <span style="font-size:10px; font-weight:700; text-transform:uppercase;
               letter-spacing:1px; padding:2px 10px; border-radius:50px;
               border:1px solid {role_color}; color:{role_color};">
            {role}
          </span>
        </div>
        """, unsafe_allow_html=True)

        # ── Nav label ─────────────────────────────────────────
        st.markdown("""
        <div style="padding:4px 20px 6px; font-size:9px; color:#1E293B;
             font-weight:700; letter-spacing:2px; text-transform:uppercase;">
          Navigation
        </div>
        """, unsafe_allow_html=True)

        # ── Nav items ─────────────────────────────────────────
        current = st.session_state.get("app_page", "home")

        for icon, label, key in NAV:
            if current == key:
                st.markdown(f"""
                <div style="margin:0 8px; padding:10px 14px; border-radius:10px;
                     background:linear-gradient(135deg,rgba(124,58,237,0.25),rgba(79,140,255,0.1));
                     border:1px solid rgba(124,58,237,0.38);
                     display:flex; align-items:center; gap:10px;
                     color:#C4B5FD; font-size:14px; font-weight:700;">
                  <span>{icon}</span>
                  <span>{label}</span>
                  <span style="margin-left:auto; width:5px; height:5px; border-radius:50%;
                        background:#8B5CF6; box-shadow:0 0 6px #8B5CF6; flex-shrink:0;"></span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                    st.session_state["app_page"] = key
                    st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        st.divider()

        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            logout()

        st.markdown("""
        <div style="padding:12px 0 8px; text-align:center;
             font-size:10px; color:#1E293B;">
          PerformaAI v1.0 · Final Year Project
        </div>
        """, unsafe_allow_html=True)