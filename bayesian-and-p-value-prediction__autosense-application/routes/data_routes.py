from flask import Blueprint, render_template, jsonify, request
from services.dataset_service import get_dataset_summary, load_dataset

data_bp = Blueprint('data', __name__)

@data_bp.route('/data-explorer')
def data_explorer_page():
    """Dataset Explorer Screen"""
    summary = get_dataset_summary()
    return render_template('data_explorer.html', summary=summary)

@data_bp.route('/api/dataset-summary')
def api_dataset_summary():
    """API endpoint for dataset summary statistics"""
    summary = get_dataset_summary()
    return jsonify({
        'success': True,
        'summary': summary
    })

@data_bp.route('/api/dataset-records')
def api_dataset_records():
    """API endpoint for retrieving dataset rows for client-side search/charts"""
    df = load_dataset()
    limit = request.args.get('limit', default=1400, type=int)
    records = df.head(limit).to_dict(orient='records')
    return jsonify({
        'success': True,
        'total': len(df),
        'returned': len(records),
        'records': records
    })
