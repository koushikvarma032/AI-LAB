from datetime import datetime
from app.utils.extensions import db

class Repayment(db.Model):
    __tablename__ = "repayments"

    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey("loan_applications.id"), nullable=False)
    amount_paid = db.Column(db.Numeric(12, 2), nullable=False)
    transaction_reference = db.Column(db.String(64), unique=True, nullable=False)
    payment_method = db.Column(db.String(30), default="UPI")
    payment_status = db.Column(db.String(20), default="SUCCESS")
    paid_at = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship("LoanApplication", back_populates="repayments")
