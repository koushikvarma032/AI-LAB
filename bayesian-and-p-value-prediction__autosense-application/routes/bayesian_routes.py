from flask import Blueprint, render_template, request, jsonify
from services.bayesian_service import get_bayesian_graph_data, get_node_cpd_tables, query_bayesian_diagnosis

bayesian_bp = Blueprint('bayesian', __name__)

@bayesian_bp.route('/bayesian-network')
def bayesian_page():
    """Probabilistic Bayesian Network Graph Visualizer Page"""
    return render_template('bayesian.html')

@bayesian_bp.route('/api/bayesian-network')
def api_bayesian_network():
    """
    API endpoint returning Bayesian DAG structure (nodes, edges) for visualizer.
    """
    graph_data = get_bayesian_graph_data()
    return jsonify({
        'success': True,
        'graph': graph_data
    })

@bayesian_bp.route('/api/bayesian-cpd/<node_name>')
def api_bayesian_cpd(node_name):
    """
    API endpoint returning Tabular CPT for a specified node.
    """
    cpd_data = get_node_cpd_tables(node_name)
    if not cpd_data:
        return jsonify({'success': False, 'error': f'Node {node_name} not found'}), 404
    return jsonify({
        'success': True,
        'cpd': cpd_data
    })
