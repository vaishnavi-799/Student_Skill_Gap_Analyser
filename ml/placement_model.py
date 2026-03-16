import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os
from config.supabase_client import get_supabase

MODEL_PATH  = "ml/placement_model.pkl"
SCALER_PATH = "ml/scaler.pkl"
FEATURES = [
    "skill_match_score",
    "cosine_similarity",
    "cgpa",
    "college_tier",
    "project_relevance_score",
    "cert_relevance_score",
    "internship_relevance_score",
    "backlog_penalty_score",
    "num_skill_gaps",
    "readiness_score",
]


def load_training_data() -> pd.DataFrame:
    """
    Pulls student_applications table from Supabase.
    This is the ML training data with 'placed' as the target label.
    """
    supabase = get_supabase()
    resp = supabase.table("student_applications").select("*").execute()
    if not resp.data:
        raise ValueError("No training data found in student_applications table.")
    df = pd.DataFrame(resp.data)
    print(f"✅ Loaded {len(df)} rows from student_applications")
    return df


def train_placement_model(save: bool = True):
    """
    Trains a Random Forest classifier on student_applications data.
    Target: placed (0 = not placed, 1 = placed)

    Steps:
    1. Load data from Supabase
    2. Select features
    3. Min-Max normalize
    4. Train/test split (80/20)
    5. Fit Random Forest
    6. Print accuracy + report
    7. Save model + scaler to disk

    Returns: (model, scaler)
    """
    df = load_training_data()

    missing = [f for f in FEATURES + ["placed"] if f not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in training data: {missing}")

    X = df[FEATURES].fillna(0)
    y = df["placed"]

    scaler  = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_split=4,
        random_state=42,
        class_weight="balanced", 
    )
    model.fit(X_train, y_train)

    y_pred   = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n📊 Random Forest Accuracy: {accuracy * 100:.1f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Not Placed", "Placed"]))

    print("\n🔍 Feature Importance:")
    for feat, imp in sorted(zip(FEATURES, model.feature_importances_),
                            key=lambda x: x[1], reverse=True):
        bar = "█" * int(imp * 40)
        print(f"  {feat:<35} {bar} {imp:.3f}")

    if save:
        with open(MODEL_PATH,  "wb") as f: pickle.dump(model,  f)
        with open(SCALER_PATH, "wb") as f: pickle.dump(scaler, f)
        print(f"\n✅ Model saved to  {MODEL_PATH}")
        print(f"✅ Scaler saved to {SCALER_PATH}")

    return model, scaler


def load_model():
    """Load saved model and scaler from disk. Train if not found."""
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH,  "rb") as f: model  = pickle.load(f)
        with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)
        return model, scaler
    else:
        print("⚠️ No saved model found — training now...")
        return train_placement_model(save=True)


def predict_placement(
    skill_match_score: float,
    cosine_similarity: float,
    cgpa: float,
    college_tier: int,
    project_relevance_score: float,
    cert_relevance_score: float,
    internship_relevance_score: float,
    backlog_penalty_score: float,
    num_skill_gaps: int,
    readiness_score: float,
) -> float:
    """
    Predicts placement probability for a student.

    All float inputs should be in their natural range:
      - skill_match_score      : 0–1
      - cosine_similarity      : 0–1
      - cgpa                   : 0–10
      - college_tier           : 1–5
      - *_score                : 0–1
      - num_skill_gaps         : 0–N
      - readiness_score        : 0–100

    Returns: float between 0.0 and 1.0 (probability of placement)
    """
    model, scaler = load_model()

    features = np.array([[
        skill_match_score,
        cosine_similarity,
        cgpa,
        college_tier,
        project_relevance_score,
        cert_relevance_score,
        internship_relevance_score,
        backlog_penalty_score,
        num_skill_gaps,
        readiness_score,
    ]])

    features_scaled = scaler.transform(features)
    probability     = model.predict_proba(features_scaled)[0][1]  # P(placed=1)

    return round(float(probability), 4)


if __name__ == "__main__":
    train_placement_model(save=True)
