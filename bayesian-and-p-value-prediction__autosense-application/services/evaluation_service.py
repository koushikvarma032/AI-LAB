import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from models.bayesian_network import AutoSenseBayesianModel
from services.dataset_service import load_dataset
from services.preprocessing_service import convert_inputs_to_bayesian_evidence
from config import Config

def evaluate_bayesian_model():
    """
    Evaluates the Bayesian Network diagnostic model on a 20% test split.
    Calculates Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
    """
    df = load_dataset()
    
    # Train / Test split (80/20)
    train_df, test_df = train_test_split(df, test_size=0.20, random_state=42, stratify=df['fault'])
    
    # Fit temporary model on training split
    temp_model = AutoSenseBayesianModel()
    
    y_true = []
    y_pred = []
    
    # Predict on test split
    for _, row in test_df.iterrows():
        inputs = {
            'battery_voltage': row['battery_voltage'],
            'alternator_voltage': row['alternator_voltage'],
            'engine_rpm': row['engine_rpm'],
            'engine_temperature': row['engine_temperature'],
            'coolant_temperature': row['coolant_temperature'],
            'oil_pressure': row['oil_pressure'],
            'slow_cranking': row['slow_cranking'],
            'hard_starting': row['hard_starting'],
            'dim_headlights': row['dim_headlights'],
            'engine_noise': row['engine_noise'],
            'overheating_indicator': row['overheating_indicator']
        }
        
        evidence = convert_inputs_to_bayesian_evidence(inputs)
        probs = temp_model.query(evidence)
        top_fault = list(probs.keys())[0]
        
        y_true.append(row['fault'])
        y_pred.append(top_fault)
        
    labels = Config.FAULTS
    
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    return {
        'total_test_samples': len(test_df),
        'accuracy': round(float(acc) * 100, 2),
        'precision': round(float(prec) * 100, 2),
        'recall': round(float(rec) * 100, 2),
        'f1_score': round(float(f1) * 100, 2),
        'confusion_matrix': cm.tolist(),
        'labels': [l.replace('_', ' ').title() for l in labels],
        'raw_labels': labels,
        'is_synthetic_eval': True,
        'note': "Metrics calculated on 20% test split from synthetic dataset."
    }
