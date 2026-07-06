import joblib
import os
import numpy as np
from ml.preprocess import encode_input

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_performance(input_dict: dict) -> tuple[int, float, list[float]]:
    """
    Returns (predicted_rating, top_confidence, all_probabilities).
    predicted_rating: 1-4
    top_confidence: 0.0-1.0
    all_probabilities: list of floats for each class [1,2,3,4]
    """
    model = load_model()
    df = encode_input(input_dict)
    prediction = int(model.predict(df)[0])
    probs = model.predict_proba(df)[0].tolist()
    confidence = max(probs)
    return prediction, confidence, probs
