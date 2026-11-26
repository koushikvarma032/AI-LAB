"""
College Student Academic Early-Warning System: Model Training & Comparative Analysis
Trains and benchmarks k-NN, Decision Tree, Naive Bayes, and Perceptron models
on early semester indicators (study time, failures, absences, parental education, G1, G2).
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sklearn reference models
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier as SklearnDT
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron as SklearnPerceptron

from src.data_loader import load_and_preprocess_data, EARLY_INDICATORS
from src.custom_models import (
    KNNClassifier,
    DecisionTreeClassifier,
    GaussianNaiveBayesClassifier,
    PerceptronClassifier
)
from src.evaluate import compute_metrics, print_evaluation_report

def run_comparison():
    print("=" * 70)
    print(" COLLEGE STUDENT ACADEMIC EARLY-WARNING SYSTEM")
    print(" AI Model Comparison: k-NN, Decision Tree, Naive Bayes, Perceptron")
    print("=" * 70)

    # 1. Load data
    data_dict = load_and_preprocess_data(csv_path="data/student_academic_records.csv")
    X_train = data_dict["X_train"]
    X_test = data_dict["X_test"]
    y_train = data_dict["y_train"]
    y_test = data_dict["y_test"]

    print(f"\n[+] Dataset loaded:")
    print(f"    Total samples: {len(data_dict['df_raw'])}")
    print(f"    Training samples: {len(y_train)} | Test samples: {len(y_test)}")
    print(f"    Features analyzed ({len(EARLY_INDICATORS)}): {', '.join(EARLY_INDICATORS)}")
    print(f"    Target: Pass (G3 >= 10, Class 1) vs Fail (G3 < 10, Class 0)")

    # 2. Define custom and benchmark models
    models = {
        "k-NN (Custom)": KNNClassifier(k=5),
        "Decision Tree (Custom)": DecisionTreeClassifier(max_depth=4, min_samples_split=4),
        "Naive Bayes (Custom)": GaussianNaiveBayesClassifier(),
        "Perceptron (Custom)": PerceptronClassifier(learning_rate=0.01, n_epochs=150),
        "k-NN (Scikit-Learn)": KNeighborsClassifier(n_neighbors=5),
        "Decision Tree (Scikit-Learn)": SklearnDT(max_depth=4, random_state=42),
        "Naive Bayes (Scikit-Learn)": GaussianNB(),
        "Perceptron (Scikit-Learn)": SklearnPerceptron(max_iter=150, tol=1e-3, random_state=42)
    }

    results = []
    confusion_matrices = {}

    print("\n[+] Training models and evaluating on holdout test set...")
    for name, model in models.items():
        # Fit model
        model.fit(X_train, y_train)
        # Predict on test set
        y_pred = model.predict(X_test)
        
        # Metrics
        metrics = compute_metrics(y_test, y_pred)
        print_evaluation_report(name, metrics)
        
        results.append({
            "Model": name,
            "Accuracy (%)": round(metrics["Accuracy"] * 100, 2),
            "Precision": round(metrics["Precision"], 4),
            "Recall (Pass)": round(metrics["Recall"], 4),
            "F1-Score": round(metrics["F1_Score"], 4),
            "At-Risk Recall (Fail)": round(metrics["Fail_Recall"], 4),
            "TP": metrics["TP"],
            "TN": metrics["TN"],
            "FP": metrics["FP"],
            "FN": metrics["FN"]
        })
        confusion_matrices[name] = metrics["Confusion_Matrix"]

    results_df = pd.DataFrame(results)

    # 3. Print Comparison Table
    print("\n" + "=" * 80)
    print(" SUMMARY BENCHMARK COMPARISON TABLE")
    print("=" * 80)
    print(results_df[["Model", "Accuracy (%)", "Precision", "Recall (Pass)", "F1-Score", "At-Risk Recall (Fail)"]].to_string(index=False))
    print("=" * 80)

    # Save results to CSV
    os.makedirs("results", exist_ok=True)
    results_df.to_csv("results/model_comparison_metrics.csv", index=False)
    print("\n[+] Saved detailed metrics table to: results/model_comparison_metrics.csv")

    # 4. Generate Visualizations
    generate_comparison_plots(results_df, confusion_matrices)
    
    # 5. Advisory Recommendation Summary
    print_advisory_insights(results_df)

    return results_df


def generate_comparison_plots(results_df, confusion_matrices):
    """Generates visual charts comparing model performance and confusion matrices."""
    os.makedirs("results", exist_ok=True)

    # Filter to main 4 models for clean charts
    main_models = ["k-NN (Custom)", "Decision Tree (Custom)", "Naive Bayes (Custom)", "Perceptron (Custom)"]
    plot_df = results_df[results_df["Model"].isin(main_models)].copy()
    plot_df["Short_Name"] = ["k-NN", "Decision Tree", "Naive Bayes", "Perceptron"]

    # 1. Bar plot of Accuracy and F1-Score
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(plot_df))
    width = 0.28

    rects1 = ax.bar(x - width, plot_df["Accuracy (%)"] / 100, width, label='Accuracy', color='#2563eb')
    rects2 = ax.bar(x, plot_df["F1-Score"], width, label='F1-Score', color='#10b981')
    rects3 = ax.bar(x + width, plot_df["At-Risk Recall (Fail)"], width, label='At-Risk Detection Rate', color='#f59e0b')

    ax.set_ylabel('Score (0.0 to 1.0)', fontsize=12, fontweight='bold')
    ax.set_title('AI Early-Warning Models Performance Comparison\n(Predicting Student Academic Success / At-Risk Status)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["Short_Name"], fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)

    for rect in rects1 + rects2 + rects3:
        h = rect.get_height()
        ax.annotate(f'{h:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig("results/model_comparison_metrics.png", dpi=300)
    plt.close()
    print("[+] Saved performance bar chart to: results/model_comparison_metrics.png")

    # 2. Confusion Matrices Subplot Grid
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    axes = axes.flatten()

    for idx, model_name in enumerate(main_models):
        cm = confusion_matrices[model_name]
        ax = axes[idx]
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, cbar=False,
                    xticklabels=['Fail (0)', 'Pass (1)'],
                    yticklabels=['Fail (0)', 'Pass (1)'],
                    annot_kws={"size": 14, "weight": "bold"})
        ax.set_title(f"{model_name}", fontsize=13, fontweight='bold')
        ax.set_xlabel('Predicted Label', fontsize=11)
        ax.set_ylabel('Actual Label', fontsize=11)

    plt.suptitle("Confusion Matrices (Test Set Predictions)", fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig("results/confusion_matrices.png", dpi=300)
    plt.close()
    print("[+] Saved confusion matrices chart to: results/confusion_matrices.png")


def print_advisory_insights(results_df):
    best_acc = results_df.loc[results_df["Accuracy (%)"].idxmax()]
    best_risk = results_df.loc[results_df["At-Risk Recall (Fail)"].idxmax()]
    
    print("\n" + "=" * 80)
    print(" ACADEMIC ADVISOR ACTIONABLE TAKEAWAYS")
    print("=" * 80)
    print(f"[*] Top Overall Accuracy Model: {best_acc['Model']} ({best_acc['Accuracy (%)']}%)")
    print(f"[*] Highest At-Risk Detection Model: {best_risk['Model']} ({best_risk['At-Risk Recall (Fail)'] * 100:.1f}%)")
    print("""
Key Early Warning Triggers:
1. Low Mid-term / Quiz Scores (G1, G2 < 10): Strongest direct correlation with final failure.
2. High Past Failures (failures >= 1): Amplifies probability of falling behind.
3. High Absences (> 8 class sessions missed): Key behavioral indicator for early intervention.
4. Low Weekly Study Time (< 2 hours): Primary target for academic mentoring coaching.

Mentoring Action Plan:
- Low-Risk Students (Pass Prob > 80%): Regular milestone check-in.
- Moderate-Risk Students: Peer-tutoring & study-habit advisory sessions.
- High-Risk Students (Predicted Fail): Immediate mandatory faculty mentoring, tutoring,
  and customized recovery milestones 4-6 weeks prior to final exams.
""")
    print("=" * 80)


if __name__ == "__main__":
    run_comparison()
