"""
home/home_view.py
------------------
The main dashboard shown after login.
Displays KPI cards, dataset insights, and quick actions.
"""
import streamlit as st
import pandas as pd
import joblib, os

from components.design_system import inject_css
from components.charts import (
    performance_distribution_chart,
    feature_importance_chart,
    correlation_heatmap,
    department_avg_chart,
    salary_vs_performance,
)
from database.models import get_stats

_BASE      = os.path.dirname(__file__)
DATA_PATH  = os.path.join(_BASE, "..", "data", "employee_data.csv")
MODEL_PATH = os.path.join(_BASE, "..", "ml", "model.pkl")
COLS_PATH  = os.path.join(_BASE, "..", "ml", "feature_columns.pkl")


@st.cache_data
def _data():
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def _model():
    return joblib.load(MODEL_PATH), joblib.load(COLS_PATH)


# ─────────────────────────────────────────────────────────────
def _kpi_html(icon, value, label):
    return f"""
    <div class="kpi-card">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
    </div>"""


def _quick_action(icon, title, desc, page_key):
    if st.button(f"{icon}  {title}", key=f"qa_{page_key}", use_container_width=True, type="primary"):
        st.session_state["app_page"] = page_key
        st.rerun()
    st.markdown(f'<div style="font-size:12px;color:#475569;text-align:center;margin-top:4px;">{desc}</div>',
                unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
def show():
    inject_css()

    name     = st.session_state.get("name", "HR Manager")
    username = st.session_state.get("username", "")
    df       = _data()
    model, feature_columns = _model()
    db       = get_stats(username)

    # computed helpers
    overtime_pct = (df["OverTime"] == "Yes").mean()
    top_dept     = df.groupby("Department")["PerformanceRating"].mean().idxmax()
    outstanding  = (df["PerformanceRating"] == 4).sum()
    at_risk      = (df["PerformanceRating"] == 1).sum()

    # ── Page open ─────────────────────────────────────────────
    st.markdown('<div class="page-wrap" style="padding-top:16px;">', unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
      <div class="page-title">Good day, {name} 👋</div>
      <div class="page-subtitle">
        Here's your HR analytics overview — {len(df):,} employees tracked across {df['Department'].nunique()} departments.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Row 1 KPIs ────────────────────────────────────────────
    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    st.markdown(
        _kpi_html("👥", f"{len(df):,}", "Total Employees") +
        _kpi_html("💰", f"₹{int(df['MonthlyIncome'].mean()):,}", "Avg Monthly Income") +
        _kpi_html("🏢", f"{df['YearsAtCompany'].mean():.1f} yrs", "Avg Tenure") +
        _kpi_html("🔮", str(db["total"] or 0), "My Predictions"),
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 2 KPIs ────────────────────────────────────────────
    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    st.markdown(
        _kpi_html("⏱️", f"{overtime_pct:.0%}", "Overtime Rate") +
        _kpi_html("🏆", top_dept, "Top Department") +
        _kpi_html("⭐", str(outstanding), "Outstanding Employees") +
        _kpi_html("🔴", str(at_risk), "At-Risk Employees"),
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="grad-line"></div>', unsafe_allow_html=True)

    # ── Quick actions ─────────────────────────────────────────
    st.markdown('<div class="glass-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    qa1, qa2, qa3 = st.columns(3, gap="medium")
    with qa1:
        _quick_action("🔮", "New Prediction", "Predict an employee's performance rating", "prediction")
    with qa2:
        _quick_action("📋", "View History",   "See all past predictions you've made", "history")
    with qa3:
        _quick_action("👤", "My Profile",     "Update your profile and settings", "profile")

    st.markdown('<div class="grad-line"></div>', unsafe_allow_html=True)

    # ── Insights tabs ─────────────────────────────────────────
    st.markdown('<div class="glass-title">📊 Dataset Insights</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Distribution",
        "🏆 Feature Importance",
        "🔥 Correlation",
        "🏢 By Department",
        "💰 Salary vs Rating",
    ])

    with tab1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="glass-title">Performance Rating Distribution</div>', unsafe_allow_html=True)
        st.pyplot(performance_distribution_chart(df), use_container_width=True)
        st.markdown("""
        <div style="font-size:12px;color:#475569;margin-top:8px;">
          Shows how employee performance ratings are distributed across all 4 categories.
          A balanced distribution ensures model accuracy across all classes.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="glass-title">Which Factors Influence Performance Most?</div>', unsafe_allow_html=True)
        st.pyplot(feature_importance_chart(model, feature_columns), use_container_width=True)
        st.markdown("""
        <div style="font-size:12px;color:#475569;margin-top:8px;">
          The Random Forest model assigns importance scores to each input feature.
          Higher bars indicate features with more predictive power.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="glass-title">Feature Correlation Heatmap</div>', unsafe_allow_html=True)
        st.pyplot(correlation_heatmap(df), use_container_width=True)
        st.markdown("""
        <div style="font-size:12px;color:#475569;margin-top:8px;">
          Darker colors indicate stronger correlations. Values near ±1 signal
          high linear relationships between features.
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="glass-title">Average Performance Rating by Department</div>', unsafe_allow_html=True)
        st.pyplot(department_avg_chart(df), use_container_width=True)

        # department table
        dept_summary = df.groupby("Department").agg(
            Employees=("PerformanceRating", "count"),
            Avg_Rating=("PerformanceRating", "mean"),
            Outstanding=("PerformanceRating", lambda x: (x == 4).sum()),
        ).round(2).reset_index()
        dept_summary.columns = ["Department", "Employees", "Avg Rating", "Outstanding ⭐"]
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="glass-title">Monthly Income vs Performance Rating</div>', unsafe_allow_html=True)
        st.pyplot(salary_vs_performance(df), use_container_width=True)
        st.markdown("""
        <div style="font-size:12px;color:#475569;margin-top:8px;">
          Each dot is one employee. Colors correspond to performance rating:
          🔴 Low · 🟡 Good · 🟢 Excellent · ⭐ Outstanding
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Dataset summary table ─────────────────────────────────
    st.markdown('<div class="grad-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-title">🗃️ Dataset Sample</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    st.markdown(f'<div style="font-size:12px;color:#475569;margin-top:6px;">Showing 10 of {len(df):,} records</div>',
                unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Close page wrap ───────────────────────────────────────
    st.markdown('</div>', unsafe_allow_html=True)
