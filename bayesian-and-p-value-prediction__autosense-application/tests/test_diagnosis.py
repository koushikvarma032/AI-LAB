import pytest
from services.diagnosis_service import DiagnosisEngine

def test_diagnosis_engine_valid():
    engine = DiagnosisEngine()
    valid_input = {
        'battery_voltage': 10.7,
        'alternator_voltage': 11.2,
        'engine_rpm': 720,
        'engine_temperature': 91.0,
        'coolant_temperature': 92.0,
        'oil_pressure': 29.0,
        'slow_cranking': True,
        'dim_headlights': True,
        'hard_starting': True,
        'engine_noise': False
    }
    
    result = engine.process_diagnosis(valid_input)
    assert result['success'] is True
    assert result['top_fault'] == 'BATTERY_FAILURE'
    assert result['top_probability'] > 50.0
    assert 'statistical_summary' in result
    assert 'explanations' in result
    assert 'evidence_map' in result
    assert len(result['evidence_map']) > 0

def test_diagnosis_engine_invalid_input():
    engine = DiagnosisEngine()
    invalid_input = {
        'battery_voltage': -5.0, # Impossible negative battery voltage
        'alternator_voltage': 14.1,
        'engine_rpm': 'invalid_rpm'
    }
    
    result = engine.process_diagnosis(invalid_input)
    assert result['success'] is False
    assert 'error' in result
