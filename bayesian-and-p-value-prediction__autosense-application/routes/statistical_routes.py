from flask import Blueprint, render_template, request, jsonify
from config import Config
from services.statistical_service import StatisticalEngine

statistical_bp = Blueprint('statistical', __name__)
stats_engine = StatisticalEngine()

@statistical_bp.route('/statistics')
def statistics_page():
    """Statistical Lab Screen"""
    explanation = stats_engine.get_statistical_methodology_explanation()
    initial_results = stats_engine.run_all_variable_tests()
    return render_template(
        'statistics.html',
        results=initial_results,
        explanation=explanation,
        faults=Config.FAULTS,
        alpha=Config.ALPHA
    )

@statistical_bp.route('/api/statistical-analysis', methods=['POST'])
def api_statistical_analysis():
    """
    API endpoint for dynamic statistical analysis queries.
    Optionally accepts 'target_fault' parameter.
    """
    data = request.get_json() or {}
    target_fault = data.get('target_fault')
    if target_fault == 'ALL' or not target_fault:
        target_fault = None
        
    results = stats_engine.run_all_variable_tests(target_fault=target_fault)
    explanation = stats_engine.get_statistical_methodology_explanation()
    
    return jsonify({
        'success': True,
        'target_fault': target_fault or 'ALL_FAULTS',
        'alpha': Config.ALPHA,
        'results': results,
        'explanation': explanation
    })
