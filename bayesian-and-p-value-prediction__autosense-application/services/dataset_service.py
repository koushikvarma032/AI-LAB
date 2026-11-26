import os
import numpy as np
import pandas as pd
from config import Config

def generate_synthetic_dataset(n_samples=1400, seed=42):
    """
    Generates a realistic synthetic automotive fault dataset for AutoSense Nexus.
    Includes continuous sensor telemetry and binary symptom observations.
    """
    np.random.seed(seed)
    
    faults_distribution = [
        ("NO_FAULT", 0.35),
        ("BATTERY_FAILURE", 0.12),
        ("ALTERNATOR_FAILURE", 0.10),
        ("STARTER_MOTOR_FAILURE", 0.08),
        ("ENGINE_OVERHEATING", 0.10),
        ("LOW_OIL_PRESSURE", 0.08),
        ("IGNITION_SPARK_PROBLEM", 0.09),
        ("COOLING_SYSTEM_FAILURE", 0.08)
    ]
    
    fault_names, probs = zip(*faults_distribution)
    fault_choices = np.random.choice(fault_names, size=n_samples, p=probs)
    
    data = []
    
    for fault in fault_choices:
        # Defaults (Normal operating vehicle state)
        battery_v = np.random.normal(12.6, 0.3)
        alt_v = np.random.normal(14.1, 0.3)
        rpm = int(np.random.normal(800, 50))
        eng_temp = np.random.normal(88.0, 3.0)
        coolant_temp = np.random.normal(85.0, 3.0)
        oil_press = np.random.normal(45.0, 5.0)
        
        slow_cranking = np.random.choice([0, 1], p=[0.95, 0.05])
        hard_starting = np.random.choice([0, 1], p=[0.95, 0.05])
        dim_headlights = np.random.choice([0, 1], p=[0.95, 0.05])
        engine_noise = np.random.choice([0, 1], p=[0.93, 0.07])
        overheating_ind = np.random.choice([0, 1], p=[0.98, 0.02])
        
        if fault == "BATTERY_FAILURE":
            battery_v = np.random.normal(10.5, 0.6)
            alt_v = np.random.normal(12.8, 0.5)
            slow_cranking = np.random.choice([0, 1], p=[0.12, 0.88])
            hard_starting = np.random.choice([0, 1], p=[0.20, 0.80])
            dim_headlights = np.random.choice([0, 1], p=[0.15, 0.85])
            
        elif fault == "ALTERNATOR_FAILURE":
            alt_v = np.random.normal(11.2, 0.6)
            battery_v = np.random.normal(11.6, 0.5)
            dim_headlights = np.random.choice([0, 1], p=[0.25, 0.75])
            slow_cranking = np.random.choice([0, 1], p=[0.50, 0.50])
            
        elif fault == "STARTER_MOTOR_FAILURE":
            battery_v = np.random.normal(12.5, 0.3) # Battery itself is good!
            alt_v = np.random.normal(14.0, 0.3)
            slow_cranking = np.random.choice([0, 1], p=[0.08, 0.92])
            hard_starting = np.random.choice([0, 1], p=[0.10, 0.90])
            engine_noise = np.random.choice([0, 1], p=[0.40, 0.60])
            
        elif fault == "ENGINE_OVERHEATING":
            eng_temp = np.random.normal(112.0, 5.0)
            coolant_temp = np.random.normal(108.0, 5.0)
            overheating_ind = np.random.choice([0, 1], p=[0.05, 0.95])
            engine_noise = np.random.choice([0, 1], p=[0.55, 0.45])
            
        elif fault == "LOW_OIL_PRESSURE":
            oil_press = np.random.normal(12.0, 4.0)
            engine_noise = np.random.choice([0, 1], p=[0.15, 0.85])
            eng_temp = np.random.normal(96.0, 4.0)
            
        elif fault == "IGNITION_SPARK_PROBLEM":
            rpm = int(np.random.normal(520, 120))
            hard_starting = np.random.choice([0, 1], p=[0.12, 0.88])
            engine_noise = np.random.choice([0, 1], p=[0.30, 0.70])
            
        elif fault == "COOLING_SYSTEM_FAILURE":
            coolant_temp = np.random.normal(115.0, 6.0)
            eng_temp = np.random.normal(106.0, 5.0)
            overheating_ind = np.random.choice([0, 1], p=[0.08, 0.92])

        # Clip values to physically realistic boundaries
        battery_v = round(max(7.0, min(16.0, float(battery_v))), 2)
        alt_v = round(max(8.0, min(18.0, float(alt_v))), 2)
        rpm = int(max(0, min(6000, rpm)))
        eng_temp = round(max(20.0, min(140.0, float(eng_temp))), 1)
        coolant_temp = round(max(20.0, min(135.0, float(coolant_temp))), 1)
        oil_press = round(max(0.0, min(90.0, float(oil_press))), 1)
        
        data.append({
            'battery_voltage': battery_v,
            'alternator_voltage': alt_v,
            'engine_rpm': rpm,
            'engine_temperature': eng_temp,
            'coolant_temperature': coolant_temp,
            'oil_pressure': oil_press,
            'slow_cranking': int(slow_cranking),
            'hard_starting': int(hard_starting),
            'dim_headlights': int(dim_headlights),
            'engine_noise': int(engine_noise),
            'overheating_indicator': int(overheating_ind),
            'fault': fault
        })
        
    df = pd.DataFrame(data)
    
    # Ensure target directory exists
    os.makedirs(os.path.dirname(Config.DATA_PATH), exist_ok=True)
    df.to_csv(Config.DATA_PATH, index=False)
    print(f"Generated synthetic vehicle fault dataset with {len(df)} records at {Config.DATA_PATH}")
    return df

def load_dataset():
    """
    Loads dataset from CSV file. If file does not exist, generates it.
    """
    if not os.path.exists(Config.DATA_PATH):
        return generate_synthetic_dataset()
    return pd.read_csv(Config.DATA_PATH)

def get_dataset_summary():
    """
    Returns structured summary of dataset for API / UI exploration.
    """
    df = load_dataset()
    
    summary = {
        'total_records': len(df),
        'columns': list(df.columns),
        'fault_counts': df['fault'].value_counts().to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_stats': df.describe().to_dict(),
        'is_synthetic': True,
        'disclaimer': "This dataset contains simulated/synthetic vehicle sensor data generated for academic & research evaluation."
    }
    return summary
