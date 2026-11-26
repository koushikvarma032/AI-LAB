"""
Interactive Academic Early-Warning Advisor CLI Tool
Allows academic counselors to evaluate an individual student's early indicators
and obtain instant pass/fail risk assessments with targeted mentoring recommendations.
"""

import argparse
import numpy as np
from src.data_loader import load_and_preprocess_data, EARLY_INDICATORS
from src.custom_models import DecisionTreeClassifier, KNNClassifier

def get_mentoring_recommendation(prediction, indicators):
    """Generates tailored intervention strategy based on student profile."""
    recs = []
    if prediction == 0:
        recs.append("[CRITICAL] Enroll in mandatory faculty-led remedial study sessions.")
        if indicators["absences"] > 6:
            recs.append(f"[ATTENDANCE] High absences detected ({indicators['absences']}). Schedule counseling check-in.")
        if indicators["studytime"] <= 2:
            recs.append("[STUDY HABIT] Structured study schedule required: aim for at least 5-10 hours/week.")
        if indicators["G1"] < 10 or indicators["G2"] < 10:
            recs.append(f"[ACADEMIC DEFICIT] Early assessments below threshold (G1={indicators['G1']}, G2={indicators['G2']}). Assign senior student peer tutor.")
        if indicators["failures"] > 0:
            recs.append(f"[REMEDIATION] Past failures noted ({indicators['failures']}). Conduct prerequisite knowledge review.")
    else:
        recs.append("[STABLE] Student is currently on track to pass final examinations (G3 >= 10).")
        if indicators["studytime"] <= 1:
            recs.append("[RECOMMENDATION] Encourage increasing study time to build long-term retention.")
        if indicators["absences"] > 10:
            recs.append("[CAUTION] Attendance is dropping; monitor subsequent lecture participation.")

    return recs

def assess_student(args=None):
    # Train primary early-warning classifier on full dataset
    data = load_and_preprocess_data()
    X_train = data["X_train"]
    y_train = data["y_train"]
    scaler = data["scaler"]

    model = DecisionTreeClassifier(max_depth=4)
    model.fit(X_train, y_train)

    if args is None:
        # Default sample student at-risk profile
        sample = {
            "studytime": 1,   # <2 hrs
            "failures": 2,    # 2 past failures
            "absences": 12,   # 12 absences
            "Medu": 2,        # 5th-9th grade
            "Fedu": 2,        # 5th-9th grade
            "freetime": 4,    # high free time
            "goout": 4,       # high going out
            "health": 3,      # normal
            "G1": 7,          # failed first quiz
            "G2": 8           # failed mid-term
        }
    else:
        sample = {k: getattr(args, k) for k in EARLY_INDICATORS}

    features_array = np.array([[sample[k] for k in EARLY_INDICATORS]], dtype=float)
    features_scaled = scaler.transform(features_array)

    pred = model.predict(features_scaled)[0]
    status = "ON TRACK TO PASS (G3 >= 10)" if pred == 1 else "AT RISK OF FAILING (G3 < 10)"
    risk_level = "LOW RISK" if pred == 1 else "HIGH RISK - EARLY WARNING TRIGGERED"

    print("\n" + "=" * 65)
    print(" ACADEMIC EARLY-WARNING ADVISORY REPORT")
    print("=" * 65)
    print(f" Student Indicators:")
    for k, v in sample.items():
        print(f"   - {k:<12}: {v}")
    print("-" * 65)
    print(f" Evaluation Status : {status}")
    print(f" Risk Classification: {risk_level}")
    print("-" * 65)
    print(" Targeted Mentoring Recommendations:")
    recs = get_mentoring_recommendation(pred, sample)
    for r in recs:
        print(f"   * {r}")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate student early indicators")
    for feat in EARLY_INDICATORS:
        parser.add_argument(f"--{feat}", type=float, default=None)
    
    parsed = parser.parse_args()
    if any(getattr(parsed, f) is not None for f in EARLY_INDICATORS):
        # Fill missing with median defaults
        assess_student(parsed)
    else:
        print("Running demonstration on sample high-risk student profile:")
        assess_student(None)
