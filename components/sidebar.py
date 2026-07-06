import streamlit as st
from auth.auth import logout


NAV_ITEMS = [
    ("🏠", "Home",        "home"),
    ("🔮", "Prediction",  "prediction"),
    ("📋", "History",     "history"),
    ("👤", "Profile",     "profile"),
]


def render_sidebar():
    with st.sidebar:
        # ── Logo ─────────────────────────────────────────────
        st.markdown("""
        <div style="padding:28px 20px 16px; text-align:center;">
          <div style="
            font-family:'Space Grotesk',sans-serif;
            font-size:22px; font-weight:800;
            background:linear-gradient(135deg,#8B5CF6,#22D3EE);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
            margin-bottom:4px;
          ">PerformaAI</div>
          <div style="font-size:10px;color:#334155;letter-spacing:2px;text-transform:uppercase;font-weight:600;">
            HR Intelligence
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── User card ─────────────────────────────────────────
        name    = st.session_state.get("name", "User")
        role    = st.session_state.get("role", "hr")
        initial = name[0].upper() if name else "U"
        role_color = "#7C3AED" if role == "admin" else "#22D3EE"

        st.markdown(f"""
        <div style="
          margin: 0 12px 20px;
          background: linear-gradient(135deg,rgba(124,58,237,.15),rgba(34,211,238,.08));
          border:1px solid rgba(124,58,237,.3);
          border-radius:16px; padding:16px; text-align:center;
        ">
          <div style="
            width:48px;height:48px;border-radius:50%;margin:0 auto 10px;
            background:linear-gradient(135deg,#7C3AED,#22D3EE);
            display:flex;align-items:center;justify-content:center;
            font-size:20px;font-weight:800;color:#fff;
            box-shadow:0 0 20px rgba(124,58,237,.4);
          ">{initial}</div>
          <div style="font-weight:700;font-size:14px;color:#E2E8F0;">{name}</div>
          <div style="
            margin-top:6px;
            display:inline-block;
            background:rgba(124,58,237,.15);
            border:1px solid {role_color};
            color:{role_color};
            font-size:10px;font-weight:700;padding:2px 10px;
            border-radius:50px;text-transform:uppercase;letter-spacing:1px;
          ">{role}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Nav label ─────────────────────────────────────────
        st.markdown("""
        <div style="padding:0 20px 8px;font-size:10px;color:#334155;
             font-weight:700;letter-spacing:2px;text-transform:uppercase;">
          Navigation
        </div>
        """, unsafe_allow_html=True)

        # ── Nav items ─────────────────────────────────────────
        current = st.session_state.get("app_page", "home")

        for icon, label, key in NAV_ITEMS:
            active = current == key
            if active:
                st.markdown(f"""
                <div style="
                  margin:0 12px 4px;
                  background:linear-gradient(135deg,rgba(124,58,237,.3),rgba(79,140,255,.15));
                  border:1px solid rgba(124,58,237,.5);
                  border-radius:10px; padding:11px 16px;
                  display:flex;align-items:center;gap:10px;
                  color:#C4B5FD;font-size:14px;font-weight:700;
                  cursor:default;
                ">
                  <span style="font-size:16px;">{icon}</span> {label}
                  <span style="margin-left:auto;width:6px;height:6px;border-radius:50%;
                        background:#8B5CF6;box-shadow:0 0 8px #8B5CF6;"></span>
                </div>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                    st.session_state["app_page"] = key
                    st.rerun()

        # ── Divider ───────────────────────────────────────────
        st.markdown("""
        <div style="margin:16px 20px;height:1px;
             background:linear-gradient(90deg,transparent,rgba(124,58,237,.4),transparent);">
        </div>
        """, unsafe_allow_html=True)

        # ── Logout ────────────────────────────────────────────
        if st.button("🚪  Logout", key="sidebar_logout", use_container_width=True):
            logout()

        # ── Bottom branding ───────────────────────────────────
        st.markdown("""
        <div style="position:absolute;bottom:20px;left:0;right:0;
             text-align:center;font-size:10px;color:#1E293B;padding:0 20px;">
          PerformaAI v1.0 · Final Year Project
        </div>
        """, unsafe_allow_html=True)
