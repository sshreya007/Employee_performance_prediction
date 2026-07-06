import pandas as pd
import joblib
import os

ENCODERS_PATH = os.path.join(os.path.dirname(__file__), "label_encoders.pkl")
COLS_PATH     = os.path.join(os.path.dirname(__file__), "feature_columns.pkl")

CATEGORICAL_COLS = ["Department", "JobRole", "OverTime"]


def load_encoders():
    return joblib.load(ENCODERS_PATH)


def load_feature_columns():
    return joblib.load(COLS_PATH)


def encode_input(input_dict: dict) -> pd.DataFrame:
    encoders = load_encoders()
    feature_columns = load_feature_columns()
    encoded = dict(input_dict)
    for col in CATEGORICAL_COLS:
        if col in encoded:
            encoded[col] = encoders[col].transform([encoded[col]])[0]
    df = pd.DataFrame([encoded])
    return df[feature_columns]
