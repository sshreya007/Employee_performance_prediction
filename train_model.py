"""
train_model.py
----------------
Loads employee_data.csv, trains a Random Forest classifier to predict
PerformanceRating (1-4), evaluates it, and saves:
  - model.pkl          : the trained model
  - label_encoders.pkl : encoders for categorical columns
  - feature_columns.pkl: the exact column order the model expects
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# 1. Load data
df = pd.read_csv("employee_data.csv")

# 2. Encode categorical columns
categorical_cols = ["Department", "JobRole", "OverTime"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 3. Split features / target
X = df.drop(columns=["PerformanceRating"])
y = df["PerformanceRating"]

feature_columns = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Train model
model = RandomForestClassifier(
    n_estimators=200, max_depth=8, random_state=42
)
model.fit(X_train, y_train)

# 5. Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy on test set: {acc:.2%}")
print(classification_report(y_test, y_pred))

# 6. Save model + encoders + column order
joblib.dump(model, "model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(feature_columns, "feature_columns.pkl")

print("Saved model.pkl, label_encoders.pkl, feature_columns.pkl")
