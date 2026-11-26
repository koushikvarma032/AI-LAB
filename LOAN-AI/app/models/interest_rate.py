from datetime import datetime
from app.utils.extensions import db

class InterestRate(db.Model):
    __tablename__ = "interest_rates"

    id = db.Column(db.Integer, primary_key=True)
    tier_name = db.Column(db.String(50), nullable=False)
    min_credit_score = db.Column(db.Integer, default=300)
    max_credit_score = db.Column(db.Integer, default=900)
    rate_adjustment = db.Column(db.Numeric(4, 2), default=0.0)
    is_promotional_zero_interest = db.Column(db.Boolean, default=False)
    valid_until = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
