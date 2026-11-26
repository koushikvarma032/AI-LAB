import pytest
from models.bayesian_network import AutoSenseBayesianModel
from services.bayesian_service import get_bayesian_model, query_bayesian_diagnosis

def test_bayesian_model_structure():
    model = get_bayesian_model()
    assert model.model is not None
    assert len(model.model.nodes()) > 0
    assert len(model.model.edges()) > 0
    assert 'fault' in model.model.nodes()

def test_bayesian_query_inference():
    evidence = {
        'battery_voltage_state': 'LOW',
        'slow_cranking': '1',
        'dim_headlights': '1'
    }
    probs = query_bayesian_diagnosis(evidence)
    assert isinstance(probs, dict)
    assert 'BATTERY_FAILURE' in probs
    
    # Check probabilities sum to 1
    total_prob = sum(probs.values())
    assert abs(total_prob - 1.0) < 1e-4
    
    # Low battery voltage should make BATTERY_FAILURE the top probability
    top_fault = list(probs.keys())[0]
    assert top_fault in ['BATTERY_FAILURE', 'ALTERNATOR_FAILURE']
