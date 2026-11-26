from datetime import datetime
from app.utils.extensions import db

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    loan_application_id = db.Column(db.Integer, db.ForeignKey("loan_applications.id"), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # PAN, AADHAAR, SALARY_SLIP, BANK_STATEMENT
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    file_mime_type = db.Column(db.String(100), nullable=False)
    file_size_bytes = db.Column(db.Integer, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship("LoanApplication", back_populates="documents")
