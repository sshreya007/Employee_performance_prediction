import streamlit as st


def render_footer():
    st.markdown("""
    <div style="
      margin-top: 60px; padding: 20px 44px;
      border-top: 1px solid rgba(124,58,237,.12);
      background: rgba(5,0,16,.6);
      display: flex; justify-content: space-between; align-items: center;
      flex-wrap: wrap; gap: 8px;
    ">
      <span style="
        font-family:'Space Grotesk',sans-serif; font-size:15px; font-weight:700;
        background:linear-gradient(135deg,#8B5CF6,#22D3EE);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
      ">PerformaAI</span>
      <span style="font-size:12px; color:#1E293B;">
        © 2025 PerformaAI &nbsp;·&nbsp; Final Year Project &nbsp;·&nbsp; HR Analytics Platform
      </span>
    </div>
    """, unsafe_allow_html=True)
