from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.models.loan import LoanApplication, LoanStatus
from app.services.loan_service import LoanStateMachine
from app.services.notification_service import NotificationService
from app.services.eligibility_service import EligibilityService

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@role_required("admin")
def dashboard():
    status_filter = request.args.get("status")
    query = LoanApplication.query.order_by(LoanApplication.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    applications = query.all()
    all_statuses = LoanStatus.ALL_STATUSES
    return render_template("admin/panel.html", applications=applications, all_statuses=all_statuses, current_filter=status_filter)

@admin_bp.route("/application/<int:app_id>", methods=["GET", "POST"])
@login_required
@role_required("admin")
def review(app_id):
    application = LoanApplication.query.get_or_404(app_id)
    allowed_transitions = LoanStateMachine.VALID_TRANSITIONS.get(application.status, [])

    if request.method == "POST":
        target_status = request.form.get("target_status")
        comment = request.form.get("comment", "").strip()

        try:
            LoanStateMachine.transition(
                application=application,
                to_status=target_status,
                user_id=current_user.id,
                comment=comment
            )
            NotificationService.send_status_update(
                email=application.applicant.email,
                application_number=application.application_number,
                new_status=target_status,
                message=comment
            )
            flash(f"Application transitioned to {target_status} successfully.", "success")
        except ValueError as e:
            flash(str(e), "danger")

        return redirect(url_for("admin.review", app_id=application.id))

    eligibility = EligibilityService.evaluate(
        birth_date=application.applicant.date_of_birth,
        monthly_income=application.applicant.monthly_income,
        existing_obligations=application.applicant.current_obligations,
        requested_amount=application.requested_amount,
        tenure_months=application.tenure_months,
        interest_rate=application.interest_rate
    )

    return render_template(
        "admin/review.html",
        application=application,
        allowed_transitions=allowed_transitions,
        eligibility=eligibility
    )
