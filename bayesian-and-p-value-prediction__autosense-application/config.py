import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'autosense_nexus_super_secret_key_2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'vehicle_fault_data.csv')
    
    # Statistical parameters
    ALPHA = 0.05
    
    # Supported Vehicle Faults
    FAULTS = [
        "NO_FAULT",
        "BATTERY_FAILURE",
        "ALTERNATOR_FAILURE",
        "STARTER_MOTOR_FAILURE",
        "ENGINE_OVERHEATING",
        "LOW_OIL_PRESSURE",
        "IGNITION_SPARK_PROBLEM",
        "COOLING_SYSTEM_FAILURE"
    ]
    
    # Supported Continuous Variables & Normal Ranges
    VARIABLE_RANGES = {
        'battery_voltage': {'min': 8.0, 'max': 16.0, 'normal_min': 12.4, 'normal_max': 14.7, 'unit': 'V'},
        'alternator_voltage': {'min': 8.0, 'max': 18.0, 'normal_min': 13.6, 'normal_max': 14.8, 'unit': 'V'},
        'engine_rpm': {'min': 0, 'max': 7000, 'normal_min': 650, 'normal_max': 3500, 'unit': 'RPM'},
        'engine_temperature': {'min': 0, 'max': 150, 'normal_min': 80, 'normal_max': 98, 'unit': '°C'},
        'coolant_temperature': {'min': 0, 'max': 140, 'normal_min': 75, 'normal_max': 95, 'unit': '°C'},
        'oil_pressure': {'min': 0, 'max': 100, 'normal_min': 25, 'normal_max': 65, 'unit': 'PSI'}
    }
    
    # Binary Symptoms
    SYMPTOMS = [
        'slow_cranking',
        'hard_starting',
        'dim_headlights',
        'engine_noise',
        'overheating_indicator'
    ]

    DISCLAIMER_TEXT = (
        "AutoSense Nexus is an educational and decision-support prototype. "
        "Its predictions are probabilistic and should not be used as the sole basis for vehicle repair or safety decisions. "
        "Always verify suspected faults using appropriate diagnostic equipment and a qualified automotive professional."
    )
