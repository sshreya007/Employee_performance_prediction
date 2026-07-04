"""
app.py - Employee Performance Prediction App with Authentication
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# ----------------------------------------------------------------
# Page config
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Employee Performance Prediction",
    page_icon="📊",
    layout="wide",
)

# ----------------------------------------------------------------
# Load credentials and setup authenticator
# ----------------------------------------------------------------
with open("credentials.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Hash the plain-text passwords on first run and save them back
stauth.Hasher.hash_passwords(config["credentials"])

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# ----------------------------------------------------------------
# Login form
# ----------------------------------------------------------------
authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error("❌ Username or password is incorrect")
    st.stop()

elif st.session_state["authentication_status"] is None:
    st.warning("👆 Please enter your username and password to continue")
    st.info("**Demo credentials:**\n\nUsername: `admin` Password: `admin123`\n\nUsername: `hrmanager` Password: `hr1234`")
    st.stop()

elif st.session_state["authentication_status"]:

    # ----------------------------------------------------------------
    # Load model artifacts (only after login)
    # ----------------------------------------------------------------
    @st.cache_resource
    def load_artifacts():
        model = joblib.load("model.pkl")
        label_encoders = joblib.load("label_encoders.pkl")
        feature_columns = joblib.load("feature_columns.pkl")
        return model, label_encoders, feature_columns

    @st.cache_data
    def load_data():
        return pd.read_csv("employee_data.csv")

    model, label_encoders, feature_columns = load_artifacts()
    df = load_data()

    PERFORMANCE_LABELS = {
        1: "🔴 Low",
        2: "🟡 Good",
        3: "🟢 Excellent",
        4: "⭐ Outstanding",
    }

    PERFORMANCE_COLORS = {
        1: "#e74c3c",
        2: "#f39c12",
        3: "#2ecc71",
        4: "#9b59b6",
    }

    # ----------------------------------------------------------------
    # Sidebar - logout + user info + inputs
    # ----------------------------------------------------------------
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/combo-chart--v1.png", width=60)
        st.markdown(f"### 👤 Welcome, **{st.session_state['name']}**")
        authenticator.logout("Logout", "sidebar")
        st.divider()

        st.header("Employee Details")

        age = st.slider("Age", 18, 60, 30)

        department = st.selectbox(
            "Department", label_encoders["Department"].classes_
        )

        job_role = st.selectbox(
            "Job Role", label_encoders["JobRole"].classes_
        )

        monthly_income = st.number_input(
            "Monthly Income (Rs.)", min_value=15000, max_value=150000,
            value=50000, step=1000
        )

        years_at_company = st.slider("Years at Company", 0, 40, 5)

        overtime = st.selectbox(
            "OverTime", label_encoders["OverTime"].classes_
        )

        distance_from_home = st.slider("Distance From Home (km)", 1, 30, 10)

        job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)

        environment_satisfaction = st.slider(
            "Environment Satisfaction (1-4)", 1, 4, 3
        )

        work_life_balance = st.slider("Work Life Balance (1-4)", 1, 4, 3)

        training_times = st.slider("Trainings Last Year", 0, 6, 2)

        predict_btn = st.button("🔮 Predict Performance", type="primary", use_container_width=True)

    # ----------------------------------------------------------------
    # Main page header
    # ----------------------------------------------------------------
    st.title("📊 Employee Performance Prediction")
    st.caption("HR Analytics Dashboard — Predict and analyze employee performance ratings")
    st.divider()

    # ----------------------------------------------------------------
    # KPI cards
    # ----------------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Employees", len(df))
    k2.metric("Avg Monthly Income", f"Rs. {int(df['MonthlyIncome'].mean()):,}")
    k3.metric("Avg Years at Company", f"{df['YearsAtCompany'].mean():.1f} yrs")
    k4.metric("Overtime Rate", f"{(df['OverTime'] == 'Yes').mean():.0%}")

    st.divider()

    # ----------------------------------------------------------------
    # Prediction section
    # ----------------------------------------------------------------
    st.header("🔮 Prediction Result")

    if predict_btn:
        input_dict = {
            "Age": age,
            "Department": label_encoders["Department"].transform([department])[0],
            "JobRole": label_encoders["JobRole"].transform([job_role])[0],
            "MonthlyIncome": monthly_income,
            "YearsAtCompany": years_at_company,
            "OverTime": label_encoders["OverTime"].transform([overtime])[0],
            "DistanceFromHome": distance_from_home,
            "JobSatisfaction": job_satisfaction,
            "EnvironmentSatisfaction": environment_satisfaction,
            "WorkLifeBalance": work_life_balance,
            "TrainingTimesLastYear": training_times,
        }

        input_df = pd.DataFrame([input_dict])[feature_columns]
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]

        label = PERFORMANCE_LABELS.get(prediction, str(prediction))
        color = PERFORMANCE_COLORS.get(prediction, "#333")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                f"""
                <div style="background-color:{color}22; border-left: 6px solid {color};
                padding: 24px; border-radius: 10px; text-align:center;">
                    <h2 style="color:{color}; margin:0;">{label}</h2>
                    <p style="margin:0; font-size:14px; color:#555;">Predicted Performance Rating</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            prob_df = pd.DataFrame({
                "Rating": [PERFORMANCE_LABELS[r] for r in model.classes_],
                "Probability": probabilities,
            })
            fig, ax = plt.subplots(figsize=(5, 2.5))
            bars = ax.barh(prob_df["Rating"], prob_df["Probability"],
                           color=[PERFORMANCE_COLORS[r] for r in model.classes_])
            ax.set_xlim(0, 1)
            ax.set_title("Prediction Confidence")
            ax.set_xlabel("Probability")
            st.pyplot(fig)

    else:
        st.info("👈 Fill in the employee details in the sidebar and click **Predict Performance**")

    st.divider()

    # ----------------------------------------------------------------
    # Insights / Graphs
    # ----------------------------------------------------------------
    st.header("📈 Dataset Insights")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Performance Distribution",
        "🏆 Feature Importance",
        "🔥 Correlation Heatmap",
        "🏢 Department Comparison",
    ])

    with tab1:
        st.subheader("Distribution of Performance Ratings")
        counts = df["PerformanceRating"].map({1: "Low", 2: "Good", 3: "Excellent", 4: "Outstanding"}).value_counts()
        counts = counts.reindex(["Low", "Good", "Excellent", "Outstanding"])
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(counts.index, counts.values,
                      color=["#e74c3c", "#f39c12", "#2ecc71", "#9b59b6"])
        ax.set_ylabel("Number of Employees")
        ax.set_xlabel("Performance Rating")
        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3,
                    str(val), ha="center", fontsize=11, fontweight="bold")
        st.pyplot(fig)

    with tab2:
        st.subheader("Which Factors Influence Performance Most?")
        importances = pd.Series(model.feature_importances_, index=feature_columns)
        importances = importances.sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        importances.plot(kind="barh", ax=ax, color="#4C72B0")
        ax.set_xlabel("Importance Score")
        ax.set_title("Random Forest Feature Importance")
        st.pyplot(fig)

    with tab3:
        st.subheader("Correlation Between Numeric Features")
        numeric_df = df.select_dtypes(include="number")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f",
                    cmap="coolwarm", ax=ax, linewidths=0.5)
        st.pyplot(fig)

    with tab4:
        st.subheader("Average Performance Rating by Department")
        dept_avg = df.groupby("Department")["PerformanceRating"].mean().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = plt.cm.viridis([x / 4 for x in dept_avg.values])
        ax.barh(dept_avg.index, dept_avg.values, color=colors)
        ax.set_xlabel("Average Performance Rating")
        ax.set_xlim(0, 4)
        for i, (val, name) in enumerate(zip(dept_avg.values, dept_avg.index)):
            ax.text(val + 0.05, i, f"{val:.2f}", va="center")
        st.pyplot(fig)

    st.divider()
    st.caption("Employee Performance Prediction System  | HR Analytics Dashboard")