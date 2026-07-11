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
        # ── Logo ──────────────────────────────────────────────
        st.markdown("""
        <div style="padding:28px 20px 12px; text-align:center;">
          <div style="font-family:'Space Grotesk',sans-serif; font-size:21px; font-weight:800;
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
        name    = st.session_state.get("name", "User")
        role    = st.session_state.get("role", "hr")
        initial = name[0].upper() if name else "U"
        role_color = "#7C3AED" if role == "admin" else "#22D3EE"

        st.markdown(f"""
        <div style="margin:0 12px 16px; padding:16px;
             background:linear-gradient(135deg,rgba(124,58,237,0.12),rgba(34,211,238,0.06));
             border:1px solid rgba(124,58,237,0.25); border-radius:14px; text-align:center;">
          <div style="width:44px; height:44px; border-radius:50%; margin:0 auto 10px;
               background:linear-gradient(135deg,#7C3AED,#22D3EE);
               display:flex; align-items:center; justify-content:center;
               font-size:18px; font-weight:800; color:#fff;
               box-shadow:0 0 18px rgba(124,58,237,0.4);">
            {initial}
          </div>
          <div style="font-weight:700; font-size:14px; color:#E2E8F0; margin-bottom:6px;">
            {name}
          </div>
          <span style="font-size:10px; font-weight:700; text-transform:uppercase;
               letter-spacing:1.2px; padding:3px 10px; border-radius:50px;
               border:1px solid {role_color}; color:{role_color};
               background:rgba(124,58,237,0.08);">
            {role}
          </span>
        </div>
        """, unsafe_allow_html=True)

        # ── Nav label ─────────────────────────────────────────
        st.markdown("""
        <div style="padding:0 18px 6px; font-size:10px; color:#1E293B;
             font-weight:700; letter-spacing:2px; text-transform:uppercase;">
          Navigation
        </div>
        """, unsafe_allow_html=True)

        # ── Nav items ─────────────────────────────────────────
        current = st.session_state.get("app_page", "home")

        for icon, label, key in NAV:
            if current == key:
                # Active item — styled inline since CSS can't target nth button
                st.markdown(f"""
                <div style="margin:2px 10px; padding:11px 16px; border-radius:10px;
                     background:linear-gradient(135deg,rgba(124,58,237,0.28),rgba(79,140,255,0.12));
                     border:1px solid rgba(124,58,237,0.4);
                     display:flex; align-items:center; gap:10px;
                     color:#C4B5FD; font-size:14px; font-weight:700; cursor:default;">
                  <span>{icon}</span> {label}
                  <span style="margin-left:auto; width:6px; height:6px; border-radius:50%;
                        background:#8B5CF6; box-shadow:0 0 8px #8B5CF6;"></span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                    st.session_state["app_page"] = key
                    st.rerun()

        st.divider()

        # ── Logout ────────────────────────────────────────────
        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            logout()

        # ── Version ───────────────────────────────────────────
        st.markdown("""
        <div style="position:absolute; bottom:16px; left:0; right:0;
             text-align:center; font-size:10px; color:#1E293B;">
          PerformaAI v1.0 · Final Year Project
        </div>
        """, unsafe_allow_html=True)
