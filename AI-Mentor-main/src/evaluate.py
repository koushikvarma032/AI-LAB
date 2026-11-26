"""
Evaluation and Comparison Metrics for AI Models
Academic Early-Warning Systems require careful consideration of False Negatives
(students predicted to Pass who actually Fail, missing timely mentoring).
"""

import numpy as np

def compute_metrics(y_true, y_pred):
    """
    Computes classification metrics:
    - Accuracy
    - Precision (Pass class)
    - Recall / Sensitivity (Pass class)
    - F1-Score
    - Specificity (True Negative Rate / Fail detection rate)
    - Confusion Matrix [ [TN, FP], [FN, TP] ]
    """
    y_true = np.array(y_true, dtype=int)
    y_pred = np.array(y_pred, dtype=int)

    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))

    accuracy = (tp + tn) / len(y_true) if len(y_true) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    fail_recall = specificity # Recall of the Fail/At-Risk group

    return {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1_Score": f1,
        "Fail_Recall": fail_recall,
        "TP": int(tp),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "Confusion_Matrix": np.array([[tn, fp], [fn, tp]])
    }

def print_evaluation_report(model_name, metrics):
    print(f"\n========================================================")
    print(f" Model: {model_name}")
    print(f"========================================================")
    print(f"  Accuracy:         {metrics['Accuracy']:.4f} ({metrics['Accuracy']*100:.2f}%)")
    print(f"  Precision (Pass): {metrics['Precision']:.4f}")
    print(f"  Recall (Pass):    {metrics['Recall']:.4f}")
    print(f"  F1-Score:         {metrics['F1_Score']:.4f}")
    print(f"  At-Risk Recall:   {metrics['Fail_Recall']:.4f} (Identified {metrics['TN']}/{metrics['TN']+metrics['FP']} failing students)")
    print(f"  Confusion Matrix:")
    print(f"               Pred Fail (0)   Pred Pass (1)")
    print(f"   Actual Fail:      {metrics['TN']:<10}   {metrics['FP']:<10}")
    print(f"   Actual Pass:      {metrics['FN']:<10}   {metrics['TP']:<10}")
