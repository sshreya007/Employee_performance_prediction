import streamlit as st


def render_topbar():
    name    = st.session_state.get("name", "User")
    role    = st.session_state.get("role", "hr").upper()
    initial = name[0].upper() if name else "U"

    st.markdown(f"""
    <div style="
      background: rgba(9,0,20,0.9);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(124,58,237,0.18);
      padding: 14px 36px;
      display: flex; align-items: center; justify-content: space-between;
    ">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:18px; font-weight:800;
        background:linear-gradient(135deg,#8B5CF6,#22D3EE);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
        PerformaAI
      </div>
      <div style="display:flex; align-items:center; gap:14px;">
        <div style="font-size:11px; color:#334155; font-weight:600;
          background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.2);
          padding:3px 10px; border-radius:50px; letter-spacing:1px; text-transform:uppercase;">
          {role}
        </div>
        <div style="width:34px; height:34px; border-radius:50%;
          background:linear-gradient(135deg,#7C3AED,#22D3EE);
          display:flex; align-items:center; justify-content:center;
          font-size:13px; font-weight:800; color:#fff;
          box-shadow:0 0 14px rgba(124,58,237,0.4);">
          {initial}
        </div>
        <div style="font-size:14px; font-weight:600; color:#C4B5FD;">{name}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
