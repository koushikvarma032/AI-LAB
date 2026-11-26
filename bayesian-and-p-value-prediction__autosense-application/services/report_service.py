import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import Config

def generate_pdf_report(diag_result):
    """
    Generates a professional diagnostic PDF report for AutoSense Nexus using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    CYAN_PRIMARY = colors.HexColor('#06b6d4')
    DARK_BG = colors.HexColor('#0f172a')
    DARK_SURFACE = colors.HexColor('#1e293b')
    TEXT_LIGHT = colors.HexColor('#f8fafc')
    TEXT_MUTED = colors.HexColor('#94a3b8')
    RED_ACCENT = colors.HexColor('#ef4444')
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=CYAN_PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=CYAN_PRIMARY,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#64748b'),
        spaceBefore=10
    )
    
    story = []
    
    # Document Header
    story.append(Paragraph("AUTOSENSE NEXUS", title_style))
    story.append(Paragraph("Intelligent Vehicle Fault Diagnosis & Statistical Analysis Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=CYAN_PRIMARY, spaceAfter=15))
    
    # Summary Header Box
    top_fault = diag_result.get('top_fault_label', 'Unknown')
    top_prob = diag_result.get('top_probability', 0.0)
    timestamp = diag_result.get('timestamp', '')
    
    header_data = [
        [Paragraph("<b>DIAGNOSED PRIMARY FAULT</b>", body_style), Paragraph("<b>POSTERIOR PROBABILITY</b>", body_style), Paragraph("<b>DIAGNOSTIC DATE</b>", body_style)],
        [Paragraph(f"<font color='#06b6d4' size=14><b>{top_fault}</b></font>", body_style), Paragraph(f"<font color='#10b981' size=14><b>{top_prob}%</b></font>", body_style), Paragraph(f"<b>{timestamp}</b>", body_style)]
    ]
    header_table = Table(header_data, colWidths=[2.5*inch, 2.2*inch, 2.3*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # Section 1: Telemetry Inputs & Symptoms
    story.append(Paragraph("1. VEHICLE TELEMETRY & OBSERVED SYMPTOMS", h2_style))
    inputs = diag_result.get('inputs', {})
    
    telemetry_data = [
        ["Parameter", "Observed Value", "Status"],
        ["Battery Voltage", f"{inputs.get('battery_voltage', 'N/A')} V", diag_result['sensor_statuses']['battery']['state']],
        ["Alternator Voltage", f"{inputs.get('alternator_voltage', 'N/A')} V", diag_result['sensor_statuses']['alternator']['state']],
        ["Engine RPM", f"{inputs.get('engine_rpm', 'N/A')} RPM", diag_result['sensor_statuses']['rpm']['state']],
        ["Engine Temperature", f"{inputs.get('engine_temperature', 'N/A')} °C", diag_result['sensor_statuses']['engine_temp']['state']],
        ["Coolant Temperature", f"{inputs.get('coolant_temperature', 'N/A')} °C", diag_result['sensor_statuses']['coolant']['state']],
        ["Oil Pressure", f"{inputs.get('oil_pressure', 'N/A')} PSI", diag_result['sensor_statuses']['oil_pressure']['state']],
    ]
    
    t_table = Table(telemetry_data, colWidths=[3.0*inch, 2.0*inch, 2.0*inch])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 12))
    
    # Symptoms List
    symptoms = [
        ("Slow Cranking", inputs.get('slow_cranking')),
        ("Hard Starting", inputs.get('hard_starting')),
        ("Dim Headlights", inputs.get('dim_headlights')),
        ("Engine Noise", inputs.get('engine_noise')),
        ("Overheating Warning", inputs.get('overheating_indicator'))
    ]
    sym_str = ", ".join([name for name, val in symptoms if val]) or "None Reported"
    story.append(Paragraph(f"<b>Observed Symptoms:</b> {sym_str}", body_style))
    story.append(Spacer(1, 15))
    
    # Section 2: Statistical Hypothesis Testing Results
    story.append(Paragraph("2. STATISTICAL HYPOTHESIS TESTING (p-value Analysis)", h2_style))
    story.append(Paragraph("Statistical hypothesis tests evaluate variable associations against α = 0.05 threshold.", body_style))
    
    stat_summary = diag_result.get('statistical_summary', {})
    sig_vars = stat_summary.get('significant_variables', [])
    
    stat_table_data = [["Variable", "Statistical Test", "Calculated p-value", "Significance (α = 0.05)"]]
    for sv in sig_vars:
        stat_table_data.append([sv['label'], sv['test'], sv['p_value'], "STATISTICALLY SIGNIFICANT"])
        
    s_table = Table(stat_table_data, colWidths=[2.2*inch, 2.2*inch, 1.4*inch, 1.2*inch])
    s_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(s_table)
    story.append(Spacer(1, 15))
    
    # Section 3: Bayesian Probabilistic Diagnosis
    story.append(Paragraph("3. BAYESIAN NETWORK POSTERIOR PROBABILITIES", h2_style))
    alts = diag_result.get('alternative_hypotheses', [])
    
    bayes_data = [["Fault Candidate", "Posterior Probability P(Fault | Evidence)"]]
    bayes_data.append([diag_result.get('top_fault_label'), f"{top_prob}% (MOST PROBABLE)"])
    for alt in alts[:4]:
        bayes_data.append([alt['label'], f"{alt['probability']}%"])
        
    b_table = Table(bayes_data, colWidths=[4.0*inch, 3.0*inch])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(b_table)
    story.append(Spacer(1, 15))
    
    # Section 4: Explainable AI Rationale
    story.append(Paragraph("4. EXPLAINABLE AI RATIONALE", h2_style))
    exps = diag_result.get('explanations', {})
    for fact in exps.get('observational_facts', []):
        story.append(Paragraph(f"• {fact}", body_style))
    story.append(Paragraph(f"<b>Statistical Rationale:</b> {exps.get('statistical_rationale', '')}", body_style))
    story.append(Paragraph(f"<b>Bayesian Propagation:</b> {exps.get('bayesian_rationale', '')}", body_style))
    story.append(Spacer(1, 15))
    
    # Section 5: Safety Disclaimer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=10))
    story.append(Paragraph(f"<b>SAFETY DISCLAIMER:</b> {Config.DISCLAIMER_TEXT}", disclaimer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
