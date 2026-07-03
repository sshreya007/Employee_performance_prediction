"""
generate_data.py
-----------------
Creates a synthetic "employee performance" dataset and saves it as
employee_data.csv. This stands in for a real HR dataset (e.g. the
IBM HR Analytics dataset on Kaggle) so the project can run fully
offline without any external downloads.

--------------

The columns and rough relationships are designed so that a machine
learning model trained on them gives sensible, explainable results.

"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 1000  # number of employee records

departments = ["Sales", "R&D", "HR", "IT", "Finance"]
job_roles = {
    "Sales": ["Sales Executive", "Sales Manager"],
    "R&D": ["Research Scientist", "Lab Technician"],
    "HR": ["HR Executive", "HR Manager"],
    "IT": ["Software Engineer", "IT Support"],
    "Finance": ["Financial Analyst", "Accountant"],
}

rows = []
for _ in range(N):
    department = np.random.choice(departments)
    job_role = np.random.choice(job_roles[department])

    age = int(np.random.randint(21, 60))
    years_at_company = int(np.clip(np.random.poisson(5), 0, age - 20))
    monthly_income = int(np.random.normal(50000, 15000))
    monthly_income = max(15000, monthly_income)

    job_satisfaction = int(np.random.randint(1, 5))      # 1 (low) - 4 (high)
    work_life_balance = int(np.random.randint(1, 5))     # 1 (bad) - 4 (best)
    training_times = int(np.random.randint(0, 7))        # trainings last year
    overtime = np.random.choice(["Yes", "No"], p=[0.3, 0.7])
    distance_from_home = int(np.random.randint(1, 30))
    environment_satisfaction = int(np.random.randint(1, 5))

    # ----- build a "performance score" from the features -----
    score = 0
    score += job_satisfaction * 1.5
    score += work_life_balance * 1.2
    score += environment_satisfaction * 1.0
    score += training_times * 0.8
    score += (years_at_company / 5)
    score -= (1.5 if overtime == "Yes" else 0)
    score -= (distance_from_home / 15)
    score += np.random.normal(0, 1.5)  # noise

    rows.append({
        "Age": age,
        "Department": department,
        "JobRole": job_role,
        "MonthlyIncome": monthly_income,
        "YearsAtCompany": years_at_company,
        "OverTime": overtime,
        "DistanceFromHome": distance_from_home,
        "JobSatisfaction": job_satisfaction,
        "EnvironmentSatisfaction": environment_satisfaction,
        "WorkLifeBalance": work_life_balance,
        "TrainingTimesLastYear": training_times,
        "_score": score,
    })

df = pd.DataFrame(rows)

# Convert the continuous score into 4 balanced performance rating
# bands using quantiles (1 = Low ... 4 = Outstanding)
df["PerformanceRating"] = pd.qcut(
    df["_score"], q=4, labels=[1, 2, 3, 4]
).astype(int)
df = df.drop(columns=["_score"])

df.to_csv("employee_data.csv", index=False)

print("Saved employee_data.csv with", len(df), "rows")
print(df["PerformanceRating"].value_counts().sort_index())
