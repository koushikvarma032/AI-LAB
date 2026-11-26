from flask import Blueprint, render_template
from config import Config
from services.evaluation_service import evaluate_bayesian_model

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    """Main Futuristic Vehicle Intelligence Command Center Dashboard"""
    return render_template('dashboard.html', faults=Config.FAULTS)

@main_bp.route('/scenarios')
def scenarios():
    """Pre-built Diagnostic Demonstration Scenarios"""
    prebuilt_scenarios = [
        {
            'id': 1,
            'title': 'Weak Battery Failure',
            'icon': 'fa-battery-quarter',
            'description': 'Battery voltage depressed (10.7 V) with slow cranking and dim headlights.',
            'inputs': {
                'battery_voltage': 10.7,
                'alternator_voltage': 12.8,
                'engine_rpm': 720,
                'engine_temperature': 91.0,
                'coolant_temperature': 92.0,
                'oil_pressure': 35.0,
                'slow_cranking': 1,
                'hard_starting': 1,
                'dim_headlights': 1,
                'engine_noise': 0,
                'overheating_indicator': 0
            }
        },
        {
            'id': 2,
            'title': 'Alternator Charging Fault',
            'icon': 'fa-bolt',
            'description': 'Alternator output inadequate (11.2 V), battery voltage dropping, dim headlights.',
            'inputs': {
                'battery_voltage': 11.5,
                'alternator_voltage': 11.2,
                'engine_rpm': 800,
                'engine_temperature': 89.0,
                'coolant_temperature': 88.0,
                'oil_pressure': 42.0,
                'slow_cranking': 0,
                'hard_starting': 0,
                'dim_headlights': 1,
                'engine_noise': 0,
                'overheating_indicator': 0
            }
        },
        {
            'id': 3,
            'title': 'Engine Overheating Thermal Crisis',
            'icon': 'fa-fire',
            'description': 'Engine & coolant temps dangerously high (115°C / 110°C) with warning active.',
            'inputs': {
                'battery_voltage': 12.6,
                'alternator_voltage': 14.1,
                'engine_rpm': 850,
                'engine_temperature': 115.0,
                'coolant_temperature': 110.0,
                'oil_pressure': 38.0,
                'slow_cranking': 0,
                'hard_starting': 0,
                'dim_headlights': 0,
                'engine_noise': 1,
                'overheating_indicator': 1
            }
        },
        {
            'id': 4,
            'title': 'Low Oil Pressure Hazard',
            'icon': 'fa-oil-can',
            'description': 'Oil pressure drops to 12.0 PSI with severe mechanical engine noise.',
            'inputs': {
                'battery_voltage': 12.6,
                'alternator_voltage': 14.0,
                'engine_rpm': 820,
                'engine_temperature': 96.0,
                'coolant_temperature': 92.0,
                'oil_pressure': 12.0,
                'slow_cranking': 0,
                'hard_starting': 0,
                'dim_headlights': 0,
                'engine_noise': 1,
                'overheating_indicator': 0
            }
        },
        {
            'id': 5,
            'title': 'Starter Motor Mechanical Jam',
            'icon': 'fa-cog',
            'description': 'Battery is healthy (12.6 V), but slow cranking (92%) & hard starting occur.',
            'inputs': {
                'battery_voltage': 12.6,
                'alternator_voltage': 14.1,
                'engine_rpm': 550,
                'engine_temperature': 88.0,
                'coolant_temperature': 85.0,
                'oil_pressure': 45.0,
                'slow_cranking': 1,
                'hard_starting': 1,
                'dim_headlights': 0,
                'engine_noise': 1,
                'overheating_indicator': 0
            }
        },
        {
            'id': 6,
            'title': 'Ignition & Spark Misfire',
            'icon': 'fa-plug',
            'description': 'Erratic idle RPM (520 RPM), hard starting, engine misfire noise.',
            'inputs': {
                'battery_voltage': 12.5,
                'alternator_voltage': 14.0,
                'engine_rpm': 520,
                'engine_temperature': 90.0,
                'coolant_temperature': 87.0,
                'oil_pressure': 42.0,
                'slow_cranking': 0,
                'hard_starting': 1,
                'dim_headlights': 0,
                'engine_noise': 1,
                'overheating_indicator': 0
            }
        }
    ]
    return render_template('scenarios.html', scenarios=prebuilt_scenarios)

@main_bp.route('/fault-library')
def fault_library():
    """Fault Library Catalog"""
    library = [
        {
            'key': 'BATTERY_FAILURE',
            'name': 'Battery Failure / Degradation',
            'severity': 'HIGH',
            'badge_color': '#ef4444',
            'symptoms': ['Slow Cranking', 'Hard Starting', 'Dim Headlights'],
            'sensors': ['Battery Voltage < 12.0 V'],
            'inspection_area': 'Battery terminals, electrolyte fluid, internal cell resistance.',
            'causes': ['Sulfation', 'Internal short circuit', 'Extreme cold weather', 'Age degradation.']
        },
        {
            'key': 'ALTERNATOR_FAILURE',
            'name': 'Alternator Charging Failure',
            'severity': 'CRITICAL',
            'badge_color': '#dc2626',
            'symptoms': ['Dim Headlights', 'Battery Discharge', 'Electrical Flickering'],
            'sensors': ['Alternator Voltage < 13.2 V'],
            'inspection_area': 'Serpentine belt tension, diode rectifier, voltage regulator.',
            'causes': ['Worn brushes', 'Blown diode bridge', 'Loose drive belt.']
        },
        {
            'key': 'STARTER_MOTOR_FAILURE',
            'name': 'Starter Motor Failure',
            'severity': 'MEDIUM',
            'badge_color': '#f59e0b',
            'symptoms': ['Slow Cranking', 'Grinding Noise', 'Hard Starting'],
            'sensors': ['Normal Voltage with Stalled Engine RPM'],
            'inspection_area': 'Starter solenoid, pinion gear, starter relay.',
            'causes': ['Worn commutator brushes', 'Faulty solenoid contacts', 'Damaged fly wheel teeth.']
        },
        {
            'key': 'ENGINE_OVERHEATING',
            'name': 'Engine Thermal Overheating',
            'severity': 'CRITICAL',
            'badge_color': '#ef4444',
            'symptoms': ['Overheating Warning Indicator', 'Steam from Hood', 'Knocking Noise'],
            'sensors': ['Engine Temperature > 108 °C', 'Coolant Temp > 105 °C'],
            'inspection_area': 'Radiator cap, coolant leaks, cylinder head gasket.',
            'causes': ['Low coolant level', 'Thermostat stuck closed', 'Head gasket breach.']
        },
        {
            'key': 'LOW_OIL_PRESSURE',
            'name': 'Low Oil Pressure Hazard',
            'severity': 'CRITICAL',
            'badge_color': '#dc2626',
            'symptoms': ['Engine Tappet Noise', 'Oil Lamp On', 'Metallic Clatter'],
            'sensors': ['Oil Pressure < 20 PSI'],
            'inspection_area': 'Engine oil dipstick, oil pump, oil pressure sensor, filter.',
            'causes': ['Insufficient engine oil', 'Clogged oil strainer', 'Worn oil pump.']
        },
        {
            'key': 'IGNITION_SPARK_PROBLEM',
            'name': 'Ignition / Spark Misfire',
            'severity': 'MEDIUM',
            'badge_color': '#f59e0b',
            'symptoms': ['Hard Starting', 'Rough Idle', 'Engine Misfire Noise'],
            'sensors': ['Erratic Low Engine RPM'],
            'inspection_area': 'Spark plugs, ignition coils, spark plug wires.',
            'causes': ['Fouled spark plugs', 'Failed ignition coil pack', 'Corroded wiring.']
        },
        {
            'key': 'COOLING_SYSTEM_FAILURE',
            'name': 'Cooling System Component Failure',
            'severity': 'HIGH',
            'badge_color': '#ef4444',
            'symptoms': ['Coolant Temperature Rise', 'Overheating Warning'],
            'sensors': ['Coolant Temp > 105 °C'],
            'inspection_area': 'Water pump, radiator fan relay, coolant hoses.',
            'causes': ['Water pump impeller failure', 'Radiator fan motor failure.']
        }
    ]
    return render_template('fault_library.html', faults=library, disclaimer=Config.DISCLAIMER_TEXT)

@main_bp.route('/evaluation')
def evaluation():
    """Model Evaluation Dashboard"""
    eval_metrics = evaluate_bayesian_model()
    return render_template('evaluation.html', metrics=eval_metrics)
