import io
from datetime import datetime

class PDFService:
    @staticmethod
    def generate_sanction_letter(application) -> bytes:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            styles = getSampleStyleSheet()
            story = []

            title_style = ParagraphStyle(
                'TitleStyle',
                parent=styles['Heading1'],
                fontSize=20,
                leading=24,
                textColor=colors.HexColor('#0F172A'),
                alignment=1
            )
            story.append(Paragraph("LoanHub Digital Lending Platform", title_style))
            story.append(Spacer(1, 10))

            subtitle_style = ParagraphStyle(
                'SubTitle',
                parent=styles['Heading2'],
                fontSize=14,
                leading=18,
                textColor=colors.HexColor('#2563EB'),
                alignment=1
            )
            story.append(Paragraph("OFFICIAL LOAN SANCTION LETTER", subtitle_style))
            story.append(Spacer(1, 20))

            date_str = datetime.utcnow().strftime('%B %d, %Y')
            story.append(Paragraph(f"<b>Date:</b> {date_str}", styles['Normal']))
            story.append(Paragraph(f"<b>Sanction Ref:</b> LH-SANC-{application.application_number}", styles['Normal']))
            story.append(Paragraph(f"<b>Applicant:</b> {application.applicant.full_name}", styles['Normal']))
            story.append(Spacer(1, 15))

            body_text = (
                f"Dear {application.applicant.full_name},<br/><br/>"
                f"We are pleased to inform you that your application for a <b>{application.loan_type.name}</b> "
                f"has been sanctioned in accordance with LoanHub credit evaluation policies."
            )
            story.append(Paragraph(body_text, styles['Normal']))
            story.append(Spacer(1, 15))

            data = [
                ["Field", "Details"],
                ["Application Number", str(application.application_number)],
                ["Loan Scheme", str(application.loan_type.name)],
                ["Sanctioned Amount", f"INR {application.requested_amount:,.2f}"],
                ["Annual Interest Rate", f"{application.interest_rate}%"],
                ["Tenure", f"{application.tenure_months} Months"],
                ["Monthly Installment (EMI)", f"INR {application.monthly_emi:,.2f}"],
                ["Current Status", str(application.status)],
            ]

            t = Table(data, colWidths=[200, 280])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 25))

            story.append(Paragraph("<b>Authorized Signatory</b><br/>LoanHub Credit Risk Committee", styles['Normal']))
            doc.build(story)
            pdf = buffer.getvalue()
            buffer.close()
            return pdf
        except ImportError:
            # Fallback simple text-based pdf or byte buffer
            return f"LOANHUB SANCTION LETTER\nApplication: {application.application_number}\nAmount: {application.requested_amount}".encode('utf-8')
