"""
HOW TO INTEGRATE AUTH INTO YOUR EXISTING app.py
-------------------------------------------------
Add these 3 lines right after your imports, before everything else.
That's all you need to do. The landing page, login, and signup are
handled automatically by the auth module.
"""

# ── Step 1: import ──────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from auth.auth import require_auth, logout
import streamlit as st

# ── Step 2: Page config (must come first in Streamlit) ──────
st.set_page_config(
    page_title="PerformaAI — Employee Performance",
    page_icon="📊",
    layout="wide",
)

# ── Step 3: Auth gate — put this RIGHT after set_page_config ─
#   If the user is not logged in, the landing/login/signup page
#   is shown automatically and the rest of app.py is skipped.
if not require_auth():
    st.stop()

# ════════════════════════════════════════════════════════════
# EVERYTHING BELOW is your existing app.py code — unchanged.
# The user only reaches this point after a successful login.
# ════════════════════════════════════════════════════════════

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── Load artifacts ───────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model          = joblib.load("model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    feature_cols   = joblib.load("feature_columns.pkl")
    return model, label_encoders, feature_cols

@st.cache_data
def load_data():
    return pd.read_csv("employee_data.csv")

model, label_encoders, feature_columns = load_artifacts()
df = load_data()

PERFORMANCE_LABELS = {1: "🔴 Low", 2: "🟡 Good", 3: "🟢 Excellent", 4: "⭐ Outstanding"}
PERFORMANCE_COLORS = {1: "#e74c3c", 2: "#f39c12", 3: "#2ecc71", 4: "#9b59b6"}

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state['name']}")
    st.caption(f"Role: {st.session_state['role'].upper()}")
    if st.button("🚪 Logout", use_container_width=True):
        logout()   # clears session and returns to landing page
    st.divider()

    st.header("Employee Details")
    age                    = st.slider("Age", 18, 60, 30)
    department             = st.selectbox("Department", label_encoders["Department"].classes_)
    job_role               = st.selectbox("Job Role", label_encoders["JobRole"].classes_)
    monthly_income         = st.number_input("Monthly Income (Rs.)", 15000, 150000, 50000, 1000)
    years_at_company       = st.slider("Years at Company", 0, 40, 5)
    overtime               = st.selectbox("OverTime", label_encoders["OverTime"].classes_)
    distance_from_home     = st.slider("Distance From Home (km)", 1, 30, 10)
    job_satisfaction       = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
    environment_satisfaction = st.slider("Environment Satisfaction (1-4)", 1, 4, 3)
    work_life_balance      = st.slider("Work Life Balance (1-4)", 1, 4, 3)
    training_times         = st.slider("Trainings Last Year", 0, 6, 2)
    predict_btn            = st.button("🔮 Predict Performance", type="primary", use_container_width=True)

# ── Main page ────────────────────────────────────────────────
st.title("📊 Employee Performance Prediction")
st.caption("HR Analytics Dashboard")
st.divider()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Employees",    len(df))
k2.metric("Avg Monthly Income", f"Rs. {int(df['MonthlyIncome'].mean()):,}")
k3.metric("Avg Years at Company", f"{df['YearsAtCompany'].mean():.1f} yrs")
k4.metric("Overtime Rate",      f"{(df['OverTime']=='Yes').mean():.0%}")
st.divider()

# ── Prediction ───────────────────────────────────────────────
st.header("🔮 Prediction Result")

if predict_btn:
    input_dict = {
        "Age":                    age,
        "Department":             label_encoders["Department"].transform([department])[0],
        "JobRole":                label_encoders["JobRole"].transform([job_role])[0],
        "MonthlyIncome":          monthly_income,
        "YearsAtCompany":         years_at_company,
        "OverTime":               label_encoders["OverTime"].transform([overtime])[0],
        "DistanceFromHome":       distance_from_home,
        "JobSatisfaction":        job_satisfaction,
        "EnvironmentSatisfaction": environment_satisfaction,
        "WorkLifeBalance":        work_life_balance,
        "TrainingTimesLastYear":  training_times,
    }
    input_df   = pd.DataFrame([input_dict])[feature_columns]
    prediction = model.predict(input_df)[0]
    probs      = model.predict_proba(input_df)[0]
    label      = PERFORMANCE_LABELS[prediction]
    color      = PERFORMANCE_COLORS[prediction]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f'<div style="background:{color}22;border-left:6px solid {color};'
            f'padding:24px;border-radius:10px;text-align:center;">'
            f'<h2 style="color:{color};margin:0;">{label}</h2>'
            f'<p style="margin:0;font-size:14px;color:#555;">Predicted Performance Rating</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        prob_df = pd.DataFrame({
            "Rating": [PERFORMANCE_LABELS[r] for r in model.classes_],
            "Probability": probs,
        })
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.barh(prob_df["Rating"], prob_df["Probability"],
                color=[PERFORMANCE_COLORS[r] for r in model.classes_])
        ax.set_xlim(0, 1); ax.set_title("Prediction Confidence")
        st.pyplot(fig)
else:
    st.info("👈 Fill in employee details in the sidebar and click **Predict Performance**")

st.divider()

# ── Insights tabs ────────────────────────────────────────────
st.header("📈 Dataset Insights")
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performance Distribution", "🏆 Feature Importance",
    "🔥 Correlation Heatmap", "🏢 Department Comparison",
])

with tab1:
    counts = df["PerformanceRating"].map({1:"Low",2:"Good",3:"Excellent",4:"Outstanding"}).value_counts()
    counts = counts.reindex(["Low","Good","Excellent","Outstanding"])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.values, color=["#e74c3c","#f39c12","#2ecc71","#9b59b6"])
    ax.set_ylabel("Employees"); st.pyplot(fig)

with tab2:
    imp = pd.Series(model.feature_importances_, index=feature_columns).sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    imp.plot(kind="barh", ax=ax, color="#4C72B0")
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(df.select_dtypes("number").corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

with tab4:
    dept_avg = df.groupby("Department")["PerformanceRating"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(dept_avg.index, dept_avg.values, color=plt.cm.viridis([x/4 for x in dept_avg.values]))
    ax.set_xlim(0, 4); st.pyplot(fig)

st.divider()
st.caption("PerformaAI | Final Year Project | HR Analytics Dashboard")
