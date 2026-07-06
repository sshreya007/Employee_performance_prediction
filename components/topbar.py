import streamlit as st


def render_topbar():
    name = st.session_state.get("name", "User")
    role = st.session_state.get("role", "hr").upper()
    initial = name[0].upper() if name else "U"

    st.markdown(f"""
    <div style="
      position: sticky; top: 0; z-index: 999;
      background: rgba(9,0,20,.85);
      backdrop-filter: blur(24px);
      border-bottom: 1px solid rgba(124,58,237,.2);
      padding: 14px 44px;
      display: flex; align-items: center; justify-content: space-between;
    ">
      <!-- Logo -->
      <div style="
        font-family:'Space Grotesk',sans-serif; font-size:20px; font-weight:800;
        background:linear-gradient(135deg,#8B5CF6,#22D3EE);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
      ">PerformaAI</div>

      <!-- Right side -->
      <div style="display:flex; align-items:center; gap:16px;">
        <div style="
          font-size:12px; color:#475569; font-weight:500;
          background:rgba(124,58,237,.1); border:1px solid rgba(124,58,237,.25);
          padding:4px 12px; border-radius:50px;
        ">{role}</div>

        <div style="
          width:36px; height:36px; border-radius:50%;
          background:linear-gradient(135deg,#7C3AED,#22D3EE);
          display:flex; align-items:center; justify-content:center;
          font-size:14px; font-weight:800; color:#fff;
          box-shadow: 0 0 16px rgba(124,58,237,.45);
        ">{initial}</div>

        <div style="font-size:14px; font-weight:600; color:#C4B5FD;">{name}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
