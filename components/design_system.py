"""
components/design_system.py
-----------------------------
Single source of truth for ALL styles used across the dashboard.
Call inject_css() at the top of every page/feature.
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

/* ═══════════════════════════════════════════════
   RESET & BASE
═══════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .stApp {
  background: #090014 !important;
  font-family: 'Inter', sans-serif;
  color: #F1F5F9;
  overflow-x: hidden;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] {
  display: none !important;
}

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ═══════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0D001F; }
::-webkit-scrollbar-thumb { background: #7C3AED; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #8B5CF6; }

/* ═══════════════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════════════ */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; } to { opacity: 1; }
}
@keyframes glow-pulse {
  0%,100% { box-shadow: 0 0 20px rgba(124,58,237,.35); }
  50%      { box-shadow: 0 0 45px rgba(124,58,237,.7), 0 0 80px rgba(79,140,255,.2); }
}
@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes float {
  0%,100% { transform: translateY(0px); }
  50%      { transform: translateY(-8px); }
}

/* ═══════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0D001F 0%, #120028 100%) !important;
  border-right: 1px solid rgba(124,58,237,.2) !important;
  min-width: 240px !important;
}

section[data-testid="stSidebar"] > div {
  padding: 0 !important;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: none !important;
  color: #64748B !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  text-align: left !important;
  border-radius: 10px !important;
  padding: 11px 16px !important;
  width: 100% !important;
  transition: all .2s ease !important;
  margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(124,58,237,.12) !important;
  color: #C4B5FD !important;
  transform: translateX(4px) !important;
}

/* ═══════════════════════════════════════════════
   PAGE WRAPPER
═══════════════════════════════════════════════ */
.page-wrap {
  padding: 40px 44px 60px;
  min-height: calc(100vh - 68px);
  animation: fadeInUp .45s ease both;
  background:
    radial-gradient(ellipse 60% 35% at 85% 5%,  rgba(124,58,237,.09), transparent 65%),
    radial-gradient(ellipse 40% 25% at 5%  85%,  rgba(34,211,238,.05), transparent 60%),
    #090014;
}

/* ═══════════════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════════════ */
.page-header { margin-bottom: 32px; }

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px; font-weight: 800; line-height: 1.1;
  background: linear-gradient(135deg, #FFFFFF 20%, #C4B5FD 80%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 6px;
}

.page-subtitle {
  font-size: 14px; color: #475569; font-weight: 400;
}

.grad-line {
  height: 1px; margin: 28px 0;
  background: linear-gradient(90deg, transparent 0%, rgba(124,58,237,.6) 40%, rgba(34,211,238,.4) 70%, transparent 100%);
}

/* ═══════════════════════════════════════════════
   KPI CARDS
═══════════════════════════════════════════════ */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.kpi-card {
  background: linear-gradient(135deg, rgba(255,255,255,.04) 0%, rgba(124,58,237,.06) 100%);
  border: 1px solid rgba(124,58,237,.2);
  border-radius: 18px;
  padding: 24px 20px 20px;
  text-align: center;
  backdrop-filter: blur(20px);
  transition: all .3s ease;
  position: relative;
  overflow: hidden;
  cursor: default;
}
.kpi-card::after {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, #7C3AED, #22D3EE);
  opacity: 0; transition: opacity .3s;
}
.kpi-card:hover {
  border-color: rgba(124,58,237,.55);
  transform: translateY(-6px);
  box-shadow: 0 20px 50px rgba(124,58,237,.18), 0 0 0 1px rgba(124,58,237,.3);
}
.kpi-card:hover::after { opacity: 1; }

.kpi-icon { font-size: 28px; margin-bottom: 12px; display: block; }

.kpi-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 30px; font-weight: 800; line-height: 1;
  background: linear-gradient(135deg, #8B5CF6, #22D3EE);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 6px;
}

.kpi-label {
  font-size: 11px; color: #475569; font-weight: 600;
  text-transform: uppercase; letter-spacing: 1px;
}

/* ═══════════════════════════════════════════════
   GLASS CARDS
═══════════════════════════════════════════════ */
.glass {
  background: rgba(255,255,255,.03);
  border: 1px solid rgba(124,58,237,.2);
  border-radius: 20px;
  padding: 28px;
  backdrop-filter: blur(20px);
  transition: all .3s ease;
  margin-bottom: 20px;
}
.glass:hover {
  border-color: rgba(124,58,237,.45);
  box-shadow: 0 12px 40px rgba(124,58,237,.12);
}

.glass-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px; font-weight: 700; color: #C4B5FD;
  margin-bottom: 20px;
  display: flex; align-items: center; gap: 8px;
}

/* ═══════════════════════════════════════════════
   PREDICTION RESULT
═══════════════════════════════════════════════ */
.pred-result {
  border-radius: 20px; padding: 36px 28px;
  text-align: center; border-left: 5px solid;
  backdrop-filter: blur(20px);
  animation: fadeInUp .4s ease both;
}
.pred-emoji { font-size: 56px; margin-bottom: 12px; display: block; }
.pred-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px; font-weight: 800; margin-bottom: 4px;
}
.pred-sub {
  font-size: 11px; color: #64748B;
  text-transform: uppercase; letter-spacing: 1.5px;
}
.conf-pill {
  display: inline-block; margin-top: 14px;
  background: rgba(34,211,238,.1); border: 1px solid rgba(34,211,238,.4);
  color: #22D3EE; border-radius: 50px; padding: 5px 18px;
  font-size: 13px; font-weight: 700;
}

/* ═══════════════════════════════════════════════
   HISTORY CARDS
═══════════════════════════════════════════════ */
.hist-card {
  background: rgba(255,255,255,.025);
  border: 1px solid rgba(124,58,237,.18);
  border-radius: 16px; padding: 18px 22px;
  margin-bottom: 10px;
  border-left: 4px solid;
  display: flex; justify-content: space-between; align-items: center;
  transition: all .25s ease;
}
.hist-card:hover {
  background: rgba(124,58,237,.07);
  border-color: rgba(124,58,237,.45);
  transform: translateX(4px);
}
.hist-emp  { font-weight: 700; font-size: 15px; color: #E2E8F0; margin-bottom: 3px; }
.hist-meta { font-size: 12px; color: #475569; }
.hist-badge {
  text-align: right;
}
.hist-badge-emoji { font-size: 24px; display: block; }
.hist-badge-label { font-size: 13px; font-weight: 700; margin-top: 2px; }
.hist-badge-conf  { font-size: 11px; color: #475569; }

/* ═══════════════════════════════════════════════
   PROFILE
═══════════════════════════════════════════════ */
.profile-banner {
  background: linear-gradient(135deg, rgba(124,58,237,.15), rgba(34,211,238,.08));
  border: 1px solid rgba(124,58,237,.3);
  border-radius: 22px; padding: 32px 36px;
  display: flex; align-items: center; gap: 28px;
  margin-bottom: 28px;
  backdrop-filter: blur(20px);
}
.profile-avatar {
  width: 80px; height: 80px; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, #7C3AED, #22D3EE);
  display: flex; align-items: center; justify-content: center;
  font-size: 34px; font-weight: 800; color: #fff;
  box-shadow: 0 0 30px rgba(124,58,237,.5);
}
.profile-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px; font-weight: 800;
  background: linear-gradient(135deg, #fff, #C4B5FD);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 3px;
}
.profile-email { font-size: 13px; color: #64748B; margin-bottom: 10px; }
.role-badge {
  display: inline-block;
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.5px; padding: 4px 14px; border-radius: 50px;
  border: 1px solid;
}

/* ═══════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
═══════════════════════════════════════════════ */
/* Inputs */
.stTextInput input,
.stNumberInput input {
  background: rgba(255,255,255,.05) !important;
  border: 1px solid rgba(124,58,237,.3) !important;
  border-radius: 10px !important;
  color: #F1F5F9 !important;
  font-size: 14px !important;
  transition: all .2s !important;
}
.stTextInput input:focus,
.stNumberInput input:focus {
  border-color: #8B5CF6 !important;
  box-shadow: 0 0 0 3px rgba(139,92,246,.15) !important;
  background: rgba(139,92,246,.07) !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder { color: #334155 !important; }

/* Selectbox */
.stSelectbox > div > div {
  background: rgba(255,255,255,.05) !important;
  border: 1px solid rgba(124,58,237,.3) !important;
  border-radius: 10px !important;
  color: #F1F5F9 !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] > div > div > div {
  background: linear-gradient(90deg, #7C3AED, #22D3EE) !important;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
  background: #8B5CF6 !important;
  border-color: #8B5CF6 !important;
  box-shadow: 0 0 12px rgba(139,92,246,.6) !important;
}

/* Primary button */
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #7C3AED, #4F8CFF) !important;
  border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; font-size: 14px !important;
  color: #fff !important; transition: all .3s !important;
  box-shadow: 0 0 24px rgba(124,58,237,.35) !important;
  padding: 10px 24px !important;
}
.stButton > button[kind="primary"]:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 45px rgba(124,58,237,.65) !important;
  filter: brightness(1.08) !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
  background: rgba(255,255,255,.04) !important;
  border: 1px solid rgba(124,58,237,.4) !important;
  border-radius: 10px !important;
  color: #8B5CF6 !important; font-weight: 600 !important;
  transition: all .2s !important;
}
.stButton > button[kind="secondary"]:hover {
  background: rgba(124,58,237,.12) !important;
  border-color: #8B5CF6 !important;
}

/* Tabs */
[data-baseweb="tab-list"] {
  background: rgba(255,255,255,.025) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid rgba(124,58,237,.18) !important;
  gap: 4px !important;
}
[data-baseweb="tab"] {
  border-radius: 8px !important;
  color: #475569 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 8px 20px !important;
  transition: all .2s !important;
}
[aria-selected="true"][data-baseweb="tab"] {
  background: linear-gradient(135deg, rgba(124,58,237,.4), rgba(79,140,255,.2)) !important;
  color: #C4B5FD !important;
}

/* Metric widgets */
[data-testid="metric-container"] {
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(124,58,237,.2) !important;
  border-radius: 14px !important;
  padding: 16px 18px !important;
}
[data-testid="metric-container"] label {
  color: #475569 !important; font-size: 12px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: #C4B5FD !important; font-weight: 800 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
  border-radius: 14px !important; overflow: hidden;
  border: 1px solid rgba(124,58,237,.2) !important;
}

/* Alerts */
[data-testid="stAlert"] { border-radius: 12px !important; }
div[data-testid="stAlert"][data-baseweb="notification"] {
  background: rgba(124,58,237,.08) !important;
  border-color: rgba(124,58,237,.35) !important;
}

/* Checkbox */
.stCheckbox label { color: #94A3B8 !important; font-size: 13px !important; }

/* Form */
[data-testid="stForm"] {
  background: rgba(255,255,255,.02) !important;
  border: 1px solid rgba(124,58,237,.18) !important;
  border-radius: 16px !important;
  padding: 24px !important;
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
