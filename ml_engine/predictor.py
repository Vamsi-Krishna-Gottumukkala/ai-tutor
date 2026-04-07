import numpy as np

LABELS = ['beginner', 'intermediate', 'advanced']
_model = None


def _get_model():
    global _model
    if _model is None:
        from ml_engine.model import load_model
        _model = load_model()
    return _model


def predict_level(score_pct: float, correct: int, wrong: int, total: int, attempt: int = 1) -> str:
    """
    Predict student skill level using Random Forest.
    Returns: 'beginner' | 'intermediate' | 'advanced'
    """
    try:
        model = _get_model()
        features = np.array([[score_pct, correct, wrong, total, attempt]])
        prediction = model.predict(features)[0]
        return LABELS[int(prediction)]
    except Exception as e:
        print(f"Prediction error: {e}")
        # Fallback to rule-based
        if score_pct < 40:
            return 'beginner'
        elif score_pct < 70:
            return 'intermediate'
        return 'advanced'


def predict_level_with_confidence(score_pct: float, correct: int, wrong: int, total: int, attempt: int = 1):
    """
    Returns: (skill_label: str, confidence_pct: float)
    """
    try:
        model = _get_model()
        features = np.array([[score_pct, correct, wrong, total, attempt]])
        prediction = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        confidence = round(float(max(proba)) * 100, 1)
        return LABELS[int(prediction)], confidence
    except Exception as e:
        print(f"Confidence prediction error: {e}")
        label = predict_level(score_pct, correct, wrong, total, attempt)
        return label, 85.0
