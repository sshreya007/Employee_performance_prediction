import streamlit as st
from auth.users import update_profile, change_password
from database.models import get_stats
from components.design_system import inject_css


def _section(title: str):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin:20px 0 12px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:15px;
           font-weight:700; color:#C4B5FD;">{title}</div>
      <div style="flex:1; height:1px;
           background:linear-gradient(90deg,rgba(124,58,237,0.4),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def show():
    inject_css()

    st.markdown("""
    <style>
    section[data-testid="stMain"] > div > div {
      padding: 28px 36px 48px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "")
    name     = st.session_state.get("name", "")
    email    = st.session_state.get("email", "")
    role     = st.session_state.get("role", "hr")
    initial  = name[0].upper() if name else "U"
    stats    = get_stats(username)
    role_color = "#7C3AED" if role == "admin" else "#22D3EE"

    # ── Header ────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:24px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:28px;
           font-weight:800; color:#F1F5F9; margin-bottom:4px;">
        👤 My Profile
      </div>
      <div style="font-size:14px; color:#475569;">
        Manage your account details and security settings.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Profile banner ────────────────────────────────────────
    st.markdown(f"""
    <div style="
      background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(34,211,238,0.06));
      border: 1px solid rgba(124,58,237,0.25);
      border-radius: 20px;
      padding: 28px 32px;
      display: flex;
      align-items: center;
      gap: 24px;
      margin-bottom: 24px;
    ">
      <div style="
        width: 72px; height: 72px; border-radius: 50%; flex-shrink: 0;
        background: linear-gradient(135deg, #7C3AED, #22D3EE);
        display: flex; align-items: center; justify-content: center;
        font-size: 28px; font-weight: 800; color: #fff;
        box-shadow: 0 0 28px rgba(124,58,237,0.45);
      ">{initial}</div>
      <div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:22px;
             font-weight:800; color:#F1F5F9; margin-bottom:4px;">{name}</div>
        <div style="font-size:13px; color:#475569; margin-bottom:10px;">{email}</div>
        <span style="
          font-size:10px; font-weight:700; text-transform:uppercase;
          letter-spacing:1.5px; padding:3px 14px; border-radius:50px;
          border:1px solid {role_color}; color:{role_color};
          background:rgba(124,58,237,0.08);
        ">{role}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────
    _section("📊 My Activity")

    c1, c2, c3, c4 = st.columns(4, gap="small")
    c1.metric("🔮  Predictions Made",  str(stats["total"] or 0))
    c2.metric("📈  Avg Rating Given",  f"{stats['avg_rating']:.2f}" if stats["avg_rating"] else "—")
    c3.metric("⭐  Outstanding Found", str(stats["outstanding"] or 0))
    c4.metric("🔴  Low Performers",    str(stats["low"] or 0))

    st.divider()

    # ── Edit / Password tabs ──────────────────────────────────
    tab1, tab2 = st.tabs(["✏️  Edit Profile", "🔑  Change Password"])

    with tab1:
        _section("Update Your Details")

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            new_name = st.text_input("Full Name", value=name, placeholder="Your full name")
        with c2:
            new_email = st.text_input("Email", value=email, placeholder="your@email.com")

        c3, c4 = st.columns(2, gap="medium")
        with c3:
            st.text_input("Username", value=username, disabled=True,
                          help="Username cannot be changed.")
        with c4:
            st.text_input("Role", value=role.upper(), disabled=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        col_save, _ = st.columns([1, 3])
        with col_save:
            if st.button("💾  Save Changes", type="primary", use_container_width=True):
                if not new_name or not new_email:
                    st.error("Name and email cannot be empty.")
                elif update_profile(username, new_name, new_email):
                    st.session_state["name"]  = new_name
                    st.session_state["email"] = new_email
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("Update failed — that email may already be in use.")

    with tab2:
        _section("Update Your Password")

        c1, c2 = st.columns(2, gap="medium")
        with c1:
            new_pw  = st.text_input("New Password", type="password",
                                    placeholder="Min. 6 characters")
        with c2:
            conf_pw = st.text_input("Confirm Password", type="password",
                                    placeholder="Repeat password")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        col_pw, _ = st.columns([1, 3])
        with col_pw:
            if st.button("🔑  Change Password", type="primary", use_container_width=True):
                if not new_pw or not conf_pw:
                    st.error("Please fill in both fields.")
                elif new_pw != conf_pw:
                    st.error("Passwords do not match.")
                elif len(new_pw) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    change_password(username, new_pw)
                    st.success("✅ Password changed successfully!")

    st.divider()

    # ── Danger zone ───────────────────────────────────────────
    _section("⚠️ Account Info")

    st.markdown(f"""
    <div style="
      background: rgba(239,68,68,0.05);
      border: 1px solid rgba(239,68,68,0.2);
      border-radius: 14px;
      padding: 20px 24px;
    ">
      <div style="font-size:14px; font-weight:600; color:#FCA5A5; margin-bottom:6px;">
        Account Details
      </div>
      <div style="font-size:13px; color:#475569; display:flex; flex-direction:column; gap:4px;">
        <span>Username: <span style="color:#94A3B8;">{username}</span></span>
        <span>Role: <span style="color:#94A3B8;">{role.upper()}</span></span>
        <span>Email: <span style="color:#94A3B8;">{email}</span></span>
      </div>
    </div>
    """, unsafe_allow_html=True)