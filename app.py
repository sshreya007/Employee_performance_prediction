"""
app.py
-------
A simple Streamlit web app that:
  1. Takes employee details as input from the user
  2. Predicts their performance rating using a pre-trained model
  3. Shows various graphs/insights from the dataset
--------
Run with:  streamlit run app.py
"""

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ----------------------------------------------------------------
# Page config
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Employee Performance Prediction",
    page_icon="📊",
    layout="wide",
)

# ----------------------------------------------------------------
# Load model, encoders, data (cached so it only runs once)
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
    1: "Low",
    2: "Good",
    3: "Excellent",
    4: "Outstanding",
}

# ----------------------------------------------------------------
# Sidebar - user inputs
# ----------------------------------------------------------------
st.sidebar.header("Enter Employee Details")

age = st.sidebar.slider("Age", 18, 60, 30)

department = st.sidebar.selectbox(
    "Department", label_encoders["Department"].classes_
)

# Job role options depend on the chosen department in the real
# IBM-style dataset, but here we simply show every role available
# to the encoder so the model always receives a valid value.
job_role = st.sidebar.selectbox(
    "Job Role", label_encoders["JobRole"].classes_
)

monthly_income = st.sidebar.number_input(
    "Monthly Income (Rs.)", min_value=15000, max_value=150000,
    value=50000, step=1000
)

years_at_company = st.sidebar.slider("Years at Company", 0, 40, 5)

overtime = st.sidebar.selectbox("OverTime", label_encoders["OverTime"].classes_)

distance_from_home = st.sidebar.slider("Distance From Home (km)", 1, 30, 10)

job_satisfaction = st.sidebar.slider("Job Satisfaction (1-4)", 1, 4, 3)

environment_satisfaction = st.sidebar.slider(
    "Environment Satisfaction (1-4)", 1, 4, 3
)

work_life_balance = st.sidebar.slider("Work Life Balance (1-4)", 1, 4, 3)

training_times = st.sidebar.slider("Trainings Last Year", 0, 6, 2)

predict_btn = st.sidebar.button("Predict Performance", type="primary")

# ----------------------------------------------------------------
# Main page
# ----------------------------------------------------------------
st.title("📊 Employee Performance Prediction")
st.write(
    "This tool predicts an employee's performance rating based on "
    "their profile, and shows insights from the overall dataset."
)

# ---------- Prediction section ----------
st.header("🔮 Prediction")

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

    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric("Predicted Performance Rating", f"{prediction} - {label}")

    with col2:
        prob_df = pd.DataFrame({
            "Rating": [f"{r} - {PERFORMANCE_LABELS[r]}" for r in model.classes_],
            "Probability": probabilities,
        })
        fig, ax = plt.subplots(figsize=(5, 2.5))
        sns.barplot(data=prob_df, x="Probability", y="Rating", ax=ax, palette="viridis")
        ax.set_xlim(0, 1)
        ax.set_title("Prediction Confidence")
        st.pyplot(fig)
else:
    st.info("Fill in the employee details on the left sidebar and click "
            "**Predict Performance** to see the result.")

# ---------- Insights / graphs section ----------
st.header("📈 Dataset Insights")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Performance Distribution", "Feature Importance", "Correlation Heatmap", "Department Comparison"]
)

with tab1:
    st.subheader("Distribution of Performance Ratings")
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["PerformanceRating"].map(PERFORMANCE_LABELS).value_counts()
    counts = counts.reindex(["Low", "Good", "Excellent", "Outstanding"])
    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="crest")
    ax.set_ylabel("Number of Employees")
    ax.set_xlabel("Performance Rating")
    st.pyplot(fig)

with tab2:
    st.subheader("Which Factors Influence Performance Most?")
    importances = pd.Series(model.feature_importances_, index=feature_columns)
    importances = importances.sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    importances.plot(kind="barh", ax=ax, color="#4C72B0")
    ax.set_xlabel("Importance")
    st.pyplot(fig)

with tab3:
    st.subheader("Correlation Between Numeric Features")
    numeric_df = df.select_dtypes(include="number")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)

with tab4:
    st.subheader("Average Performance Rating by Department")
    dept_avg = df.groupby("Department")["PerformanceRating"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=dept_avg.values, y=dept_avg.index, ax=ax, palette="flare")
    ax.set_xlabel("Average Performance Rating")
    ax.set_xlim(0, 4)
    st.pyplot(fig)

st.markdown("---")
st.caption(
    "Note: This app uses a synthetic dataset and a Random Forest model "
    "for demonstration purposes as part of a final year project."
)
