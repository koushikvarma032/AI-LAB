import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_dashboard_route(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'AUTOSENSE' in rv.data

def test_diagnostics_route(client):
    rv = client.get('/diagnostics')
    assert rv.status_code == 200
    assert b'LIVE DIAGNOSTIC' in rv.data

def test_statistics_route(client):
    rv = client.get('/statistics')
    assert rv.status_code == 200
    assert b'STATISTICAL HYPOTHESIS LAB' in rv.data

def test_bayesian_route(client):
    rv = client.get('/bayesian-network')
    assert rv.status_code == 200
    assert b'PROBABILISTIC GRAPHICAL MODEL' in rv.data

def test_data_explorer_route(client):
    rv = client.get('/data-explorer')
    assert rv.status_code == 200
    assert b'VEHICLE TELEMETRY DATA EXPLORER' in rv.data

def test_scenarios_route(client):
    rv = client.get('/scenarios')
    assert rv.status_code == 200
    assert b'DIAGNOSTIC DEMONSTRATION SCENARIOS' in rv.data

def test_fault_library_route(client):
    rv = client.get('/fault-library')
    assert rv.status_code == 200
    assert b'VEHICLE FAULT REFERENCE LIBRARY' in rv.data

def test_evaluation_route(client):
    rv = client.get('/evaluation')
    assert rv.status_code == 200
    assert b'BAYESIAN MODEL PERFORMANCE' in rv.data

def test_api_diagnose(client):
    payload = {
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
    rv = client.post('/api/diagnose', data=json.dumps(payload), content_type='application/json')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['success'] is True
    assert data['top_fault'] == 'BATTERY_FAILURE'

def test_api_bayesian_network(client):
    rv = client.get('/api/bayesian-network')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['success'] is True
    assert 'nodes' in data['graph']

def test_api_dataset_summary(client):
    rv = client.get('/api/dataset-summary')
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data['success'] is True
    assert data['summary']['total_records'] > 0

def test_api_generate_report(client):
    payload = {
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
    rv = client.post('/api/generate-report', data=json.dumps(payload), content_type='application/json')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'application/pdf'
