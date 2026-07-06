"""
Run from project root:  python data/generate_data.py
Creates data/employee_data.csv with 1000 balanced synthetic records.
"""
import os, sys
import numpy as np
import pandas as pd

OUT = os.path.join(os.path.dirname(__file__), "employee_data.csv")
np.random.seed(42)
N = 1000

departments = ["Sales", "R&D", "HR", "IT", "Finance"]
job_roles = {
    "Sales": ["Sales Executive", "Sales Manager"],
    "R&D":   ["Research Scientist", "Lab Technician"],
    "HR":    ["HR Executive", "HR Manager"],
    "IT":    ["Software Engineer", "IT Support"],
    "Finance": ["Financial Analyst", "Accountant"],
}

rows = []
for _ in range(N):
    dept     = np.random.choice(departments)
    job_role = np.random.choice(job_roles[dept])
    age      = int(np.random.randint(21, 60))
    yac      = int(np.clip(np.random.poisson(5), 0, age - 20))
    income   = max(15000, int(np.random.normal(50000, 15000)))
    js       = int(np.random.randint(1, 5))
    wlb      = int(np.random.randint(1, 5))
    train    = int(np.random.randint(0, 7))
    ot       = np.random.choice(["Yes", "No"], p=[0.3, 0.7])
    dist     = int(np.random.randint(1, 30))
    env      = int(np.random.randint(1, 5))
    score    = (js*1.5 + wlb*1.2 + env + train*.8 + yac/5
                - (1.5 if ot=="Yes" else 0) - dist/15
                + np.random.normal(0, 1.5))
    rows.append(dict(Age=age, Department=dept, JobRole=job_role,
                     MonthlyIncome=income, YearsAtCompany=yac,
                     OverTime=ot, DistanceFromHome=dist,
                     JobSatisfaction=js, EnvironmentSatisfaction=env,
                     WorkLifeBalance=wlb, TrainingTimesLastYear=train,
                     _score=score))

df = pd.DataFrame(rows)
df["PerformanceRating"] = pd.qcut(df["_score"], q=4, labels=[1,2,3,4]).astype(int)
df = df.drop(columns=["_score"])
df.to_csv(OUT, index=False)
print(f"Saved {len(df)} rows → {OUT}")
print(df["PerformanceRating"].value_counts().sort_index())
