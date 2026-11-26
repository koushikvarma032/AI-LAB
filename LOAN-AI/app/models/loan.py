from datetime import datetime
from app.utils.extensions import db

class LoanStatus:
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    DOCUMENT_VERIFICATION = "DOCUMENT_VERIFICATION"
    ELIGIBILITY_CHECK = "ELIGIBILITY_CHECK"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SANCTIONED = "SANCTIONED"
    DISBURSED = "DISBURSED"
    ACTIVE = "ACTIVE"
    REPAYMENT = "REPAYMENT"
    CLOSED = "CLOSED"

    ALL_STATUSES = [
        SUBMITTED, UNDER_REVIEW, DOCUMENT_VERIFICATION,
        ELIGIBILITY_CHECK, APPROVED, REJECTED,
        SANCTIONED, DISBURSED, ACTIVE, REPAYMENT, CLOSED
    ]

class LoanType(db.Model):
    __tablename__ = "loan_types"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    min_amount = db.Column(db.Numeric(12, 2), nullable=False)
    max_amount = db.Column(db.Numeric(12, 2), nullable=False)
    min_tenure_months = db.Column(db.Integer, nullable=False)
    max_tenure_months = db.Column(db.Integer, nullable=False)
    base_interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship("LoanApplication", back_populates="loan_type")

class LoanApplication(db.Model):
    __tablename__ = "loan_applications"

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(32), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    loan_type_id = db.Column(db.Integer, db.ForeignKey("loan_types.id"), nullable=False)
    
    requested_amount = db.Column(db.Numeric(12, 2), nullable=False)
    approved_amount = db.Column(db.Numeric(12, 2))
    tenure_months = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Numeric(5, 2), nullable=False)
    monthly_emi = db.Column(db.Numeric(12, 2))
    
    purpose = db.Column(db.String(255))
    status = db.Column(db.String(40), default=LoanStatus.SUBMITTED, nullable=False, index=True)
    rejection_reason = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applicant = db.relationship("User", back_populates="applications")
    loan_type = db.relationship("LoanType", back_populates="applications")
    status_history = db.relationship("LoanStatusHistory", back_populates="application", cascade="all, delete-orphan", order_by="LoanStatusHistory.created_at.desc()")
    documents = db.relationship("Document", back_populates="application", cascade="all, delete-orphan")
    emi_schedules = db.relationship("EMISchedule", back_populates="application", cascade="all, delete-orphan")
    repayments = db.relationship("Repayment", back_populates="application", cascade="all, delete-orphan")

class LoanStatusHistory(db.Model):
    __tablename__ = "loan_status_history"

    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey("loan_applications.id"), nullable=False)
    from_status = db.Column(db.String(40))
    to_status = db.Column(db.String(40), nullable=False)
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship("LoanApplication", back_populates="status_history")
    changed_by = db.relationship("User")
