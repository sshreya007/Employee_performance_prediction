"""
components/design_system.py
----------------------------
Styles Streamlit's OWN containers with CSS overrides.
No HTML wrapper divs. No spacing issues.
Call inject_css() at the top of every page.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

/* ═══ REMOVE STREAMLIT CHROME ═══════════════════════════════ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ═══ GLOBAL ═════════════════════════════════════════════════ */
html, body, .stApp { background: #090014 !important; }
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* Kill ALL default Streamlit padding — this is the root fix */
.main .block-container             { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"]      { padding: 0 !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stVerticalBlock"]    { gap: 0 !important; }

/* ═══ SCROLLBAR ══════════════════════════════════════════════ */
::-webkit-scrollbar                { width: 5px; }
::-webkit-scrollbar-track          { background: #0D001F; }
::-webkit-scrollbar-thumb          { background: #7C3AED; border-radius: 4px; }

/* ═══ SIDEBAR ════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: #0D001F !important;
  border-right: 1px solid rgba(124,58,237,0.18) !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
section[data-testid="stSidebar"] .stButton > button {
  all: unset;
  display: flex !important;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 11px 18px;
  font-size: 14px;
  font-weight: 500;
  color: #64748B;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.18s, color 0.18s, transform 0.18s;
  font-family: 'Inter', sans-serif !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(124,58,237,0.1) !important;
  color: #C4B5FD !important;
  transform: translateX(3px);
}

/* ═══ INPUTS ═════════════════════════════════════════════════ */
.stTextInput input, .stNumberInput input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(124,58,237,0.28) !important;
  border-radius: 10px !important;
  color: #0F0F0F !important;
  font-size: 14px !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color: #8B5CF6 !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
  background: rgba(139,92,246,0.06) !important;
}
input::placeholder { color: #334155 !important; }
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label, .stCheckbox label {
  color: #94A3B8 !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}
.stSelectbox > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(124,58,237,0.28) !important;
  border-radius: 10px !important;
  color: #F1F5F9 !important;
}
[data-baseweb="slider"] [role="slider"] {
  background: #8B5CF6 !important;
  border-color: #8B5CF6 !important;
  box-shadow: 0 0 10px rgba(139,92,246,0.5) !important;
}

/* ═══ BUTTONS ════════════════════════════════════════════════ */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #7C3AED, #4F8CFF) !important;
  border: none !important;
  border-radius: 10px !important;
  color: #fff !important;
  font-weight: 700 !important;
  font-size: 14px !important;
  padding: 11px 24px !important;
  transition: all 0.25s !important;
  box-shadow: 0 0 20px rgba(124,58,237,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 36px rgba(124,58,237,0.55) !important;
  filter: brightness(1.08) !important;
}
.stButton > button[kind="secondary"] {
  background: transparent !important;
  border: 1px solid rgba(124,58,237,0.35) !important;
  border-radius: 10px !important;
  color: #8B5CF6 !important;
  font-weight: 600 !important;
  transition: all 0.2s !important;
}
.stButton > button[kind="secondary"]:hover {
  background: rgba(124,58,237,0.1) !important;
  border-color: #8B5CF6 !important;
}

/* ═══ TABS ═══════════════════════════════════════════════════ */
[data-baseweb="tab-list"] {
  background: rgba(255,255,255,0.02) !important;
  border-radius: 10px !important;
  padding: 3px !important;
  border: 1px solid rgba(124,58,237,0.15) !important;
  gap: 2px !important;
}
[data-baseweb="tab"] {
  border-radius: 8px !important;
  color: #475569 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 7px 16px !important;
  transition: all 0.18s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  background: linear-gradient(135deg,rgba(124,58,237,0.35),rgba(79,140,255,0.18)) !important;
  color: #C4B5FD !important;
}

/* ═══ METRICS ════════════════════════════════════════════════ */
[data-testid="metric-container"] {
  background: rgba(255,255,255,0.025) !important;
  border: 1px solid rgba(124,58,237,0.18) !important;
  border-radius: 14px !important;
  padding: 18px 20px !important;
  transition: border-color 0.2s, transform 0.2s !important;
}
[data-testid="metric-container"]:hover {
  border-color: rgba(124,58,237,0.4) !important;
  transform: translateY(-2px) !important;
}
[data-testid="metric-container"] label { color: #475569 !important; font-size: 11px !important; font-weight:600 !important; text-transform:uppercase; letter-spacing:.8px; }
[data-testid="stMetricValue"] { color: #C4B5FD !important; font-weight: 800 !important; font-family:'Space Grotesk',sans-serif !important; }

/* ═══ DATAFRAME ══════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(124,58,237,0.18) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
}

/* ═══ ALERTS ═════════════════════════════════════════════════ */
[data-testid="stAlert"]  { border-radius: 10px !important; font-size: 13px !important; }
.stSuccess { background: rgba(16,185,129,0.08) !important; border-color: rgba(16,185,129,0.35) !important; }
.stError   { background: rgba(239,68,68,0.08) !important;  border-color: rgba(239,68,68,0.35) !important;  }
.stInfo    { background: rgba(79,140,255,0.08) !important; border-color: rgba(79,140,255,0.35) !important; }

/* ═══ FORM ═══════════════════════════════════════════════════ */
[data-testid="stForm"] {
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(124,58,237,0.15) !important;
  border-radius: 14px !important;
  padding: 20px !important;
}

/* ═══ HR DIVIDER ═════════════════════════════════════════════ */
hr {
  border: none !important;
  height: 1px !important;
  background: linear-gradient(90deg,transparent,rgba(124,58,237,0.5),rgba(34,211,238,0.3),transparent) !important;
  margin: 16px 0 !important;
}

/* ═══ ANIMATIONS ═════════════════════════════════════════════ */
@keyframes fadeInUp    { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes glow-pulse  { 0%,100%{box-shadow:0 0 18px rgba(124,58,237,.35)} 50%{box-shadow:0 0 40px rgba(124,58,237,.65)} }
@keyframes grad-shift  { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
