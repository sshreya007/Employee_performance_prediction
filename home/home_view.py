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


def _section(title: str):
    """Renders a clean section label."""
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin:28px 0 14px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:15px;
           font-weight:700; color:#C4B5FD;">{title}</div>
      <div style="flex:1; height:1px;
           background:linear-gradient(90deg,rgba(124,58,237,0.4),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def show():
    inject_css()

    # Page padding via CSS on the main content area
    st.markdown("""
    <style>
    /* Content area padding — applied once here, not via wrapper div */
    section[data-testid="stMain"] > div > div {
      padding: 28px 36px 48px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    name     = st.session_state.get("name", "HR Manager")
    username = st.session_state.get("username", "")
    df       = _data()
    model, feature_columns = _model()
    db       = get_stats(username)

    # ── Page header ───────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:24px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:28px;
           font-weight:800; color:#F1F5F9; margin-bottom:4px;">
        Good day, {name} 👋
      </div>
      <div style="font-size:14px; color:#475569;">
        {len(df):,} employees tracked across {df['Department'].nunique()} departments.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI row 1 ─────────────────────────────────────────────
    _section("Overview")
    c1, c2, c3, c4 = st.columns(4, gap="small")
    c1.metric("👥  Total Employees",    f"{len(df):,}")
    c2.metric("💰  Avg Monthly Income", f"₹{int(df['MonthlyIncome'].mean()):,}")
    c3.metric("🏢  Avg Tenure",         f"{df['YearsAtCompany'].mean():.1f} yrs")
    c4.metric("🔮  My Predictions",     str(db["total"] or 0))

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── KPI row 2 ─────────────────────────────────────────────
    top_dept = df.groupby("Department")["PerformanceRating"].mean().idxmax()
    c5, c6, c7, c8 = st.columns(4, gap="small")
    c5.metric("⏱️  Overtime Rate",       f"{(df['OverTime']=='Yes').mean():.0%}")
    c6.metric("🏆  Top Department",      top_dept)
    c7.metric("⭐  Outstanding",         str(int((df["PerformanceRating"]==4).sum())))
    c8.metric("🔴  At-Risk",             str(int((df["PerformanceRating"]==1).sum())))

    st.divider()

    # ── Quick actions ─────────────────────────────────────────
    _section("⚡ Quick Actions")
    qa1, qa2, qa3 = st.columns(3, gap="small")

    with qa1:
        st.markdown("""
        <div style="background:rgba(124,58,237,0.08); border:1px solid rgba(124,58,237,0.2);
             border-radius:14px; padding:18px 20px; margin-bottom:8px;">
          <div style="font-size:22px; margin-bottom:8px;">🔮</div>
          <div style="font-weight:700; font-size:14px; color:#E2E8F0; margin-bottom:4px;">New Prediction</div>
          <div style="font-size:12px; color:#475569;">Predict an employee's performance rating</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Prediction →", key="qa_pred", use_container_width=True, type="primary"):
            st.session_state["app_page"] = "prediction"; st.rerun()

    with qa2:
        st.markdown("""
        <div style="background:rgba(79,140,255,0.06); border:1px solid rgba(79,140,255,0.18);
             border-radius:14px; padding:18px 20px; margin-bottom:8px;">
          <div style="font-size:22px; margin-bottom:8px;">📋</div>
          <div style="font-weight:700; font-size:14px; color:#E2E8F0; margin-bottom:4px;">View History</div>
          <div style="font-size:12px; color:#475569;">See all past predictions you've made</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to History →", key="qa_hist", use_container_width=True):
            st.session_state["app_page"] = "history"; st.rerun()

    with qa3:
        st.markdown("""
        <div style="background:rgba(34,211,238,0.05); border:1px solid rgba(34,211,238,0.15);
             border-radius:14px; padding:18px 20px; margin-bottom:8px;">
          <div style="font-size:22px; margin-bottom:8px;">👤</div>
          <div style="font-weight:700; font-size:14px; color:#E2E8F0; margin-bottom:4px;">My Profile</div>
          <div style="font-size:12px; color:#475569;">Update your account settings</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Profile →", key="qa_prof", use_container_width=True):
            st.session_state["app_page"] = "profile"; st.rerun()

    st.divider()

    # ── Charts ────────────────────────────────────────────────
    _section("📊 Dataset Insights")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Distribution",
        "Feature Importance",
        "Correlation",
        "By Department",
        "Salary vs Rating",
    ])

    with tab1:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.pyplot(performance_distribution_chart(df), use_container_width=True)
        st.caption("Distribution of performance ratings across all 4 categories.")

    with tab2:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.pyplot(feature_importance_chart(model, feature_columns), use_container_width=True)
        st.caption("Higher bars = more predictive power in the Random Forest model.")

    with tab3:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.pyplot(correlation_heatmap(df), use_container_width=True)
        st.caption("Values near ±1 indicate strong linear relationships between features.")

    with tab4:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.pyplot(department_avg_chart(df), use_container_width=True)
        dept_summary = df.groupby("Department").agg(
            Employees=("PerformanceRating","count"),
            Avg_Rating=("PerformanceRating","mean"),
            Outstanding=("PerformanceRating", lambda x:(x==4).sum()),
        ).round(2).reset_index()
        dept_summary.columns = ["Department","Employees","Avg Rating","Outstanding ⭐"]
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)

    with tab5:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.pyplot(salary_vs_performance(df), use_container_width=True)
        st.caption("🔴 Low · 🟡 Good · 🟢 Excellent · ⭐ Outstanding")

    st.divider()

    # ── Dataset sample ────────────────────────────────────────
    _section("🗃️ Dataset Sample")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    st.caption(f"Showing 10 of {len(df):,} records.")
