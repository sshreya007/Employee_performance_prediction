"""
Run from the project root:   python ml/train_model.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

DATA_PATH     = os.path.join(os.path.dirname(__file__), "..", "data", "employee_data.csv")
MODEL_PATH    = os.path.join(os.path.dirname(__file__), "model.pkl")
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), "label_encoders.pkl")
COLS_PATH     = os.path.join(os.path.dirname(__file__), "feature_columns.pkl")

CATEGORICAL_COLS = ["Department", "JobRole", "OverTime"]


def train():
    df = pd.read_csv(DATA_PATH)
    label_encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    X = df.drop(columns=["PerformanceRating"])
    y = df["PerformanceRating"]
    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Accuracy: {acc:.2%}")

    joblib.dump(model,          MODEL_PATH)
    joblib.dump(label_encoders, ENCODERS_PATH)
    joblib.dump(feature_columns, COLS_PATH)
    print("Model saved to ml/")


if __name__ == "__main__":
    train()
