import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os
from django.conf import settings

LABELS = ['beginner', 'intermediate', 'advanced']
MODEL_PATH = str(settings.ML_MODEL_PATH)


def generate_synthetic_data(n_samples: int = 2000):
    """
    Generate synthetic training data.
    Features: [score_pct, correct_count, wrong_count, total_questions, attempt_number]
    Labels: 0=beginner, 1=intermediate, 2=advanced
    """
    np.random.seed(42)
    data, labels = [], []

    for _ in range(n_samples):
        total = np.random.randint(5, 15)
        score_pct = np.random.uniform(0, 100)
        correct = int(total * score_pct / 100)
        wrong = total - correct
        attempt = np.random.randint(1, 30)

        data.append([score_pct, correct, wrong, total, attempt])

        # Classification threshold
        if score_pct < 40:
            labels.append(0)  # Beginner
        elif score_pct < 70:
            labels.append(1)  # Intermediate
        else:
            labels.append(2)  # Advanced

    return np.array(data), np.array(labels)


def train_model(use_real_data: bool = True):
    """Train Random Forest and save to disk."""
    X_synth, y_synth = generate_synthetic_data()

    if use_real_data:
        try:
            from assessments.models import QuizAttempt
            real_attempts = QuizAttempt.objects.all()
            real_X, real_y = [], []

            label_map = {'beginner': 0, 'intermediate': 1, 'advanced': 2}

            for a in real_attempts:
                label = label_map.get(a.skill_level, 0)
                real_X.append([
                    a.percentage,
                    a.score,
                    a.total_questions - a.score,
                    a.total_questions,
                    1,
                ])
                real_y.append(label)

            if real_X:
                real_X = np.array(real_X)
                real_y = np.array(real_y)
                # Combine synthetic + real data (weight real data more)
                X_combined = np.vstack([X_synth, real_X, real_X, real_X])
                y_combined = np.hstack([y_synth, real_y, real_y, real_y])
                X_train, X_test, y_train, y_test = train_test_split(
                    X_combined, y_combined, test_size=0.2, random_state=42
                )
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_synth, y_synth, test_size=0.2, random_state=42
                )
        except Exception as e:
            print(f"Could not load real data: {e}")
            X_train, X_test, y_train, y_test = train_test_split(
                X_synth, y_synth, test_size=0.2, random_state=42
            )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X_synth, y_synth, test_size=0.2, random_state=42
        )

    clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    clf.fit(X_train, y_train)
    accuracy = clf.score(X_test, y_test)
    print(f"✅ Random Forest trained — Test Accuracy: {accuracy:.2%}")

    # Ensure directory exists
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")
    return clf


def load_model():
    """Load trained model from disk, training if not present."""
    if not os.path.exists(MODEL_PATH):
        print("⚠️  Model not found. Training now...")
        return train_model(use_real_data=False)
    return joblib.load(MODEL_PATH)
