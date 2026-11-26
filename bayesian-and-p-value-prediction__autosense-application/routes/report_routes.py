from flask import Blueprint, request, make_response, jsonify
from services.diagnosis_service import DiagnosisEngine
from services.report_service import generate_pdf_report

report_bp = Blueprint('report', __name__)
engine = DiagnosisEngine()

@report_bp.route('/api/generate-report', methods=['POST'])
def api_generate_report():
    """
    API Endpoint for ReportLab PDF Diagnostic Report generation.
    """
    data = request.get_json() or request.form.to_dict()
    
    # Process diagnosis
    diag_result = engine.process_diagnosis(data)
    if not diag_result['success']:
        return jsonify({'success': False, 'error': diag_result['error']}), 400
        
    # Generate PDF binary bytes
    pdf_bytes = generate_pdf_report(diag_result)
    
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=AutoSense_Nexus_Diagnostic_Report.pdf'
    return response
