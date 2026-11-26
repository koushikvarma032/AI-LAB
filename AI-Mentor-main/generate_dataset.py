import os
import numpy as np
import pandas as pd

def generate_student_dataset(n_samples=600, random_state=42, output_path="data/student_academic_records.csv"):
    """
    Generates a realistic toy dataset for College Student Academic Early-Warning System.
    Modeled after the UCI Student Performance benchmark dataset.
    
    Indicators:
    - studytime: Weekly study time (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h)
    - failures: Number of past semester course failures (0, 1, 2, 3, 4)
    - absences: Number of class absences (0 to 30)
    - Medu: Mother's education level (0: None, 1: Primary, 2: 5th-9th, 3: Secondary, 4: Higher Ed)
    - Fedu: Father's education level (0: None, 1: Primary, 2: 5th-9th, 3: Secondary, 4: Higher Ed)
    - freetime: Free time after classes (1: Very low to 5: Very high)
    - goout: Going out with friends (1: Very low to 5: Very high)
    - health: Current health status (1: Very bad to 5: Very good)
    - G1: Early-semester assessment score (0 - 20 scale)
    - G2: Mid-semester assessment score (0 - 20 scale)
    - G3: Final semester grade (0 - 20 scale)
    - Pass_Fail: 1 if G3 >= 10 (Pass), 0 if G3 < 10 (Fail)
    """
    np.random.seed(random_state)
    
    # 1. Background demographic & habits
    studytime = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.25, 0.45, 0.20, 0.10])
    failures = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.75, 0.15, 0.07, 0.03])
    absences = np.clip(np.random.negative_binomial(2, 0.2, size=n_samples), 0, 32)
    Medu = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.05, 0.15, 0.25, 0.30, 0.25])
    Fedu = np.random.choice([0, 1, 2, 3, 4], size=n_samples, p=[0.05, 0.20, 0.25, 0.30, 0.20])
    freetime = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.15, 0.50, 0.20, 0.10])
    goout = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.10, 0.20, 0.35, 0.25, 0.10])
    health = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.05, 0.10, 0.25, 0.30, 0.30])
    
    # 2. Early-semester indicators G1 & G2 with realistic correlations
    # Academic latent capability factor
    academic_latent = (
        1.8 * studytime 
        - 2.4 * failures 
        - 0.15 * absences 
        + 0.5 * Medu 
        + 0.4 * Fedu 
        - 0.3 * (goout - 3)
        + 0.2 * (health - 3)
        + np.random.normal(0, 1.8, size=n_samples)
    )
    
    # Base score centered around 11
    base_g1 = 11.0 + academic_latent * 0.9 + np.random.normal(0, 1.5, size=n_samples)
    G1 = np.clip(np.round(base_g1), 0, 20).astype(int)
    
    # G2 depends heavily on G1 and continuing habits
    base_g2 = 0.75 * G1 + 0.35 * academic_latent + 2.0 + np.random.normal(0, 1.2, size=n_samples)
    G2 = np.clip(np.round(base_g2), 0, 20).astype(int)
    
    # G3 is final grade
    base_g3 = 0.5 * G1 + 0.45 * G2 + 0.2 * academic_latent + np.random.normal(0, 1.0, size=n_samples)
    # Failure penalty if past failures > 1
    base_g3 -= failures * 0.8
    G3 = np.clip(np.round(base_g3), 0, 20).astype(int)
    
    # Pass threshold: G3 >= 10 (Standard European/Portuguese 20-point academic grading)
    Pass_Fail = (G3 >= 10).astype(int)
    
    df = pd.DataFrame({
        "studytime": studytime,
        "failures": failures,
        "absences": absences,
        "Medu": Medu,
        "Fedu": Fedu,
        "freetime": freetime,
        "goout": goout,
        "health": health,
        "G1": G1,
        "G2": G2,
        "G3": G3,
        "Pass_Fail": Pass_Fail
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated dataset with {len(df)} records at: {output_path}")
    print(f"Pass/Fail distribution: Pass={sum(Pass_Fail==1)} ({sum(Pass_Fail==1)/len(df):.1%}), Fail={sum(Pass_Fail==0)} ({sum(Pass_Fail==0)/len(df):.1%})")
    return df

if __name__ == "__main__":
    generate_student_dataset(output_path="data/student_academic_records.csv")
