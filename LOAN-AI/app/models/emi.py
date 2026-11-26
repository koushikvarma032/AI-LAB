from datetime import date
from app.utils.extensions import db

class EMISchedule(db.Model):
    __tablename__ = "emi_schedules"

    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey("loan_applications.id"), nullable=False)
    installment_number = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    opening_balance = db.Column(db.Numeric(12, 2), nullable=False)
    principal_component = db.Column(db.Numeric(12, 2), nullable=False)
    interest_component = db.Column(db.Numeric(12, 2), nullable=False)
    total_installment = db.Column(db.Numeric(12, 2), nullable=False)
    closing_balance = db.Column(db.Numeric(12, 2), nullable=False)
    is_paid = db.Column(db.Boolean, default=False)
    paid_at = db.Column(db.Date)

    application = db.relationship("LoanApplication", back_populates="emi_schedules")
