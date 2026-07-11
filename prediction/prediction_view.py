import streamlit as st
import joblib, os
from ml.predict import predict_performance
from ml.preprocess import load_encoders
from database.models import save_prediction
from components.design_system import inject_css
from components.charts import confidence_bar_chart
from utils.helpers import PERFORMANCE_LABELS, rating_color

EMOJI = {1: "🔴", 2: "🟡", 3: "🟢", 4: "⭐"}


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

    encoders = load_encoders()

    # ── Header ────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:24px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:28px;
           font-weight:800; color:#F1F5F9; margin-bottom:4px;">
        🔮 Performance Prediction
      </div>
      <div style="font-size:14px; color:#475569;">
        Fill in the employee details below to get an AI-powered performance rating.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Employee Info ─────────────────────────────────────────
    _section("👤 Employee Information")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        emp_name   = st.text_input("Employee Name (optional)", placeholder="e.g. John Doe")
        age        = st.slider("Age", 18, 60, 30)
        department = st.selectbox("Department", encoders["Department"].classes_)
    with c2:
        job_role         = st.selectbox("Job Role", encoders["JobRole"].classes_)
        monthly_income   = st.number_input("Monthly Income (Rs.)", 15000, 150000, 50000, 1000)
        years_at_company = st.slider("Years at Company", 0, 40, 5)
    with c3:
        overtime           = st.selectbox("OverTime", encoders["OverTime"].classes_)
        distance_from_home = st.slider("Distance From Home (km)", 1, 30, 10)
        job_satisfaction   = st.slider("Job Satisfaction (1–4)", 1, 4, 3)

    st.divider()

    _section("📊 Satisfaction Scores")

    c4, c5, c6 = st.columns(3, gap="medium")
    with c4:
        env_satisfaction  = st.slider("Environment Satisfaction (1–4)", 1, 4, 3)
    with c5:
        work_life_balance = st.slider("Work Life Balance (1–4)", 1, 4, 3)
    with c6:
        training_times    = st.slider("Trainings Last Year", 0, 6, 2)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Submit ────────────────────────────────────────────────
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        submitted = st.button("🔮  Predict Performance", use_container_width=True, type="primary")

    # ── Result ────────────────────────────────────────────────
    if submitted:
        input_dict = {
            "Age": age,
            "Department": department,
            "JobRole": job_role,
            "MonthlyIncome": monthly_income,
            "YearsAtCompany": years_at_company,
            "OverTime": overtime,
            "DistanceFromHome": distance_from_home,
            "JobSatisfaction": job_satisfaction,
            "EnvironmentSatisfaction": env_satisfaction,
            "WorkLifeBalance": work_life_balance,
            "TrainingTimesLastYear": training_times,
        }

        with st.spinner("Running AI model…"):
            prediction, confidence, probs = predict_performance(input_dict)

        label = PERFORMANCE_LABELS[prediction]
        color = rating_color(prediction)
        emoji = EMOJI[prediction]

        st.divider()
        _section("✅ Prediction Result")

        res_col, chart_col = st.columns([1, 2], gap="large")

        with res_col:
            st.markdown(f"""
            <div style="
              background:{color}12;
              border:1px solid {color}60;
              border-left:5px solid {color};
              border-radius:16px;
              padding:28px 22px;
              text-align:center;
            ">
              <div style="font-size:52px; margin-bottom:10px;">{emoji}</div>
              <div style="font-family:'Space Grotesk',sans-serif; font-size:26px;
                   font-weight:800; color:{color}; margin-bottom:4px;">{label}</div>
              <div style="font-size:11px; color:#64748B; text-transform:uppercase;
                   letter-spacing:1.5px; margin-bottom:14px;">Performance Rating</div>
              <div style="display:inline-block; background:rgba(34,211,238,0.1);
                   border:1px solid rgba(34,211,238,0.35); color:#22D3EE;
                   border-radius:50px; padding:5px 18px;
                   font-size:13px; font-weight:700;">
                {confidence:.0%} confidence
              </div>
            </div>
            """, unsafe_allow_html=True)

        with chart_col:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(124,58,237,0.18);
                 border-radius:14px; padding:20px;">
              <div style="font-size:13px; font-weight:600; color:#C4B5FD; margin-bottom:12px;">
                Confidence per Rating
              </div>
            """, unsafe_allow_html=True)
            model_obj = joblib.load(
                os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
            )
            fig = confidence_bar_chart(model_obj.classes_, probs)
            st.pyplot(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Summary metrics ───────────────────────────────────
        st.divider()
        _section("📋 Employee Summary")

        m1, m2, m3, m4 = st.columns(4, gap="small")
        m1.metric("Age",             age)
        m2.metric("Department",      department)
        m3.metric("Income",          f"₹{monthly_income:,}")
        m4.metric("Years at Company",f"{years_at_company} yrs")

        m5, m6, m7, m8 = st.columns(4, gap="small")
        m5.metric("Job Satisfaction",  job_satisfaction)
        m6.metric("Work Life Balance", work_life_balance)
        m7.metric("OverTime",          overtime)
        m8.metric("Trainings/Year",    training_times)

        # ── Save ──────────────────────────────────────────────
        save_prediction(
            username      = st.session_state.get("username", ""),
            employee_name = emp_name,
            department    = department,
            job_role      = job_role,
            input_data    = input_dict,
            prediction    = prediction,
            confidence    = confidence,
        )
        st.success("✅ Prediction saved to your history!")