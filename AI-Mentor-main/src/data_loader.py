"""
Data Loader & Preprocessing Pipeline
Prepares early-semester indicators for College Student Academic Early-Warning System.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Features available weeks before final examinations:
EARLY_INDICATORS = [
    "studytime",   # weekly study time
    "failures",    # past class failures
    "absences",    # lecture & tutorial absences
    "Medu",        # mother's education level
    "Fedu",        # father's education level
    "freetime",    # free time
    "goout",       # going out
    "health",      # health status
    "G1",          # early semester exam / quiz score
    "G2"           # mid-semester exam score
]

TARGET_COL = "Pass_Fail"

def load_and_preprocess_data(csv_path="data/student_academic_records.csv", test_size=0.25, random_state=42):
    """
    Loads student dataset, selects early indicators, standardizes numeric features,
    and splits into stratified train/test sets.
    """
    if not os.path.exists(csv_path):
        from generate_dataset import generate_student_dataset
        df = generate_student_dataset(output_path=csv_path)
    else:
        df = pd.read_csv(csv_path)

    X = df[EARLY_INDICATORS].copy()
    y = df[TARGET_COL].values

    # Stratified train/test split to preserve pass/fail proportions
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Standardization (essential for k-NN and Perceptron)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return {
        "X_train_raw": X_train.values,
        "X_test_raw": X_test.values,
        "X_train": X_train_scaled,
        "X_test": X_test_scaled,
        "y_train": y_train,
        "y_test": y_test,
        "feature_names": EARLY_INDICATORS,
        "scaler": scaler,
        "df_raw": df
    }
