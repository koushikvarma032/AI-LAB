from flask import Blueprint, render_template, request, jsonify
from config import Config
from services.diagnosis_service import DiagnosisEngine

diagnostic_bp = Blueprint('diagnostic', __name__)
engine = DiagnosisEngine()

@diagnostic_bp.route('/diagnostics')
def diagnostics_page():
    """Live Diagnostics Screen"""
    return render_template('diagnostics.html', ranges=Config.VARIABLE_RANGES, symptoms=Config.SYMPTOMS)

@diagnostic_bp.route('/compare')
def compare_page():
    """Diagnostic Repair Comparison Screen"""
    return render_template('compare.html', ranges=Config.VARIABLE_RANGES, symptoms=Config.SYMPTOMS)

@diagnostic_bp.route('/api/diagnose', methods=['POST'])
def api_diagnose():
    """
    API endpoint for executing diagnostic pipeline.
    Accepts JSON payload of sensor values and symptoms.
    """
    data = request.get_json() or request.form.to_dict()
    result = engine.process_diagnosis(data)
    if not result['success']:
        return jsonify(result), 400
    return jsonify(result)

@diagnostic_bp.route('/api/compare', methods=['POST'])
def api_compare():
    """
    API endpoint for comparing two diagnostic states (e.g. Before Repair vs After Repair).
    """
    data = request.get_json() or {}
    before_data = data.get('before', {})
    after_data = data.get('after', {})
    
    res_before = engine.process_diagnosis(before_data)
    res_after = engine.process_diagnosis(after_data)
    
    if not res_before['success'] or not res_after['success']:
        return jsonify({
            'success': False,
            'error': 'One or both diagnostic input sets contained invalid data.'
        }), 400
        
    # Compute probability shifts
    prob_shifts = []
    for fault in Config.FAULTS:
        p1 = res_before['posteriors'].get(fault, 0.0)
        p2 = res_after['posteriors'].get(fault, 0.0)
        shift = round(p2 - p1, 1)
        prob_shifts.append({
            'fault': fault,
            'label': fault.replace('_', ' ').title(),
            'before_prob': p1,
            'after_prob': p2,
            'shift': shift
        })
        
    prob_shifts.sort(key=lambda x: max(x['before_prob'], x['after_prob']), reverse=True)
    
    return jsonify({
        'success': True,
        'before': res_before,
        'after': res_after,
        'shifts': prob_shifts
    })
