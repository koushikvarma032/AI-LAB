import os
import uuid
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory, Response, abort
from flask_login import login_required, current_user
from app.utils.extensions import db
from app.models.loan import LoanType, LoanApplication, LoanStatus, LoanStatusHistory
from app.models.document import Document
from app.services.emi_service import EMIService
from app.services.eligibility_service import EligibilityService
from app.services.pdf_service import PDFService
from app.utils.validators import allowed_file, sanitize_filename_str

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    loan_types = LoanType.query.filter_by(is_active=True).all()
    return render_template("index.html", loan_types=loan_types)

@main_bp.route("/calculator", methods=["GET", "POST"])
def calculator():
    loan_types = LoanType.query.filter_by(is_active=True).all()
    calculation = None
    schedule = None

    if request.method == "POST":
        try:
            principal = Decimal(request.form.get("principal", "500000"))
            rate = Decimal(request.form.get("interest_rate", "10.5"))
            tenure = int(request.form.get("tenure_months", "24"))

            monthly_emi = EMIService.calculate_monthly_emi(principal, rate, tenure)
            schedule = EMIService.generate_amortization_schedule(principal, rate, tenure)[:12]  # First 12 installments preview
            total_payment = monthly_emi * tenure
            total_interest = total_payment - principal

            calculation = {
                "principal": principal,
                "rate": rate,
                "tenure": tenure,
                "monthly_emi": monthly_emi,
                "total_payment": total_payment,
                "total_interest": total_interest,
            }
        except Exception as e:
            flash(f"Calculation error: {str(e)}", "danger")

    return render_template("calculator.html", loan_types=loan_types, calculation=calculation, schedule=schedule)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    applications = LoanApplication.query.filter_by(user_id=current_user.id).order_by(LoanApplication.created_at.desc()).all()
    return render_template("dashboard.html", applications=applications)

@main_bp.route("/apply/<int:loan_type_id>", methods=["GET", "POST"])
@login_required
def apply(loan_type_id):
    loan_type = LoanType.query.get_or_404(loan_type_id)

    if request.method == "POST":
        amount = Decimal(request.form.get("amount", "0"))
        tenure = int(request.form.get("tenure_months", "12"))
        purpose = request.form.get("purpose", "").strip()

        if amount < loan_type.min_amount or amount > loan_type.max_amount:
            flash(f"Amount must be between INR {loan_type.min_amount:,.2f} and INR {loan_type.max_amount:,.2f}", "danger")
            return render_template("apply.html", loan_type=loan_type)

        if tenure < loan_type.min_tenure_months or tenure > loan_type.max_tenure_months:
            flash(f"Tenure must be between {loan_type.min_tenure_months} and {loan_type.max_tenure_months} months", "danger")
            return render_template("apply.html", loan_type=loan_type)

        monthly_emi = EMIService.calculate_monthly_emi(amount, loan_type.base_interest_rate, tenure)
        app_num = f"LH-{uuid.uuid4().hex[:8].upper()}"

        application = LoanApplication(
            application_number=app_num,
            user_id=current_user.id,
            loan_type_id=loan_type.id,
            requested_amount=amount,
            tenure_months=tenure,
            interest_rate=loan_type.base_interest_rate,
            monthly_emi=monthly_emi,
            purpose=purpose,
            status=LoanStatus.SUBMITTED
        )
        db.session.add(application)
        db.session.commit()

        # Add initial status history
        history = LoanStatusHistory(
            loan_application_id=application.id,
            from_status=None,
            to_status=LoanStatus.SUBMITTED,
            changed_by_user_id=current_user.id,
            comment="Application initially created and submitted."
        )
        db.session.add(history)
        db.session.commit()

        flash(f"Application {app_num} created successfully!", "success")
        return redirect(url_for("main.application_detail", app_id=application.id))

    return render_template("apply.html", loan_type=loan_type)

@main_bp.route("/application/<int:app_id>")
@login_required
def application_detail(app_id):
    application = LoanApplication.query.get_or_404(app_id)
    if application.user_id != current_user.id and current_user.role != "admin":
        abort(403)

    eligibility = EligibilityService.evaluate(
        birth_date=application.applicant.date_of_birth,
        monthly_income=application.applicant.monthly_income,
        existing_obligations=application.applicant.current_obligations,
        requested_amount=application.requested_amount,
        tenure_months=application.tenure_months,
        interest_rate=application.interest_rate
    )

    schedule = EMIService.generate_amortization_schedule(
        principal=application.requested_amount,
        annual_interest_rate=application.interest_rate,
        tenure_months=application.tenure_months
    )

    return render_template(
        "application_detail.html",
        application=application,
        eligibility=eligibility,
        schedule=schedule
    )

@main_bp.route("/application/<int:app_id>/upload", methods=["POST"])
@login_required
def upload_document(app_id):
    application = LoanApplication.query.get_or_404(app_id)
    if application.user_id != current_user.id:
        abort(403)

    file = request.files.get("document")
    doc_type = request.form.get("document_type", "GENERAL")

    if not file or not file.filename:
        flash("Please select a file to upload.", "warning")
        return redirect(url_for("main.application_detail", app_id=app_id))

    if not allowed_file(file.filename):
        flash("Unsupported file extension. Allowed: PDF, PNG, JPG, JPEG.", "danger")
        return redirect(url_for("main.application_detail", app_id=app_id))

    safe_name = sanitize_filename_str(file.filename)
    stored_name = f"{uuid.uuid4().hex}_{safe_name}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], stored_name)
    file.save(save_path)

    file_size = os.path.getsize(save_path)
    doc = Document(
        loan_application_id=application.id,
        document_type=doc_type,
        original_filename=safe_name,
        stored_filename=stored_name,
        file_mime_type=file.content_type or "application/octet-stream",
        file_size_bytes=file_size,
        is_verified=False
    )
    db.session.add(doc)
    db.session.commit()

    flash("Document uploaded successfully.", "success")
    return redirect(url_for("main.application_detail", app_id=app_id))

@main_bp.route("/application/<int:app_id>/sanction-letter")
@login_required
def download_sanction_letter(app_id):
    application = LoanApplication.query.get_or_404(app_id)
    if application.user_id != current_user.id and current_user.role != "admin":
        abort(403)

    pdf_bytes = PDFService.generate_sanction_letter(application)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment;filename=Sanction_Letter_{application.application_number}.pdf"}
    )
