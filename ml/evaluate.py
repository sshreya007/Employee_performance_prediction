import pandas as pd
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from ml.preprocess import CATEGORICAL_COLS, load_encoders, load_feature_columns

DATA_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "employee_data.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def get_evaluation() -> dict:
    df = pd.read_csv(DATA_PATH)
    encoders = load_encoders()
    for col in CATEGORICAL_COLS:
        df[col] = encoders[col].transform(df[col])

    feature_columns = load_feature_columns()
    X = df[feature_columns]
    y = df["PerformanceRating"]

    model = joblib.load(MODEL_PATH)
    y_pred = model.predict(X)

    return {
        "accuracy":   accuracy_score(y, y_pred),
        "report":     classification_report(y, y_pred, output_dict=True),
        "confusion":  confusion_matrix(y, y_pred).tolist(),
        "classes":    model.classes_.tolist(),
        "importance": dict(zip(feature_columns, model.feature_importances_.tolist())),
    }
