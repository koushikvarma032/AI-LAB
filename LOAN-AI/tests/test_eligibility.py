from decimal import Decimal
from datetime import date
from app.services.eligibility_service import EligibilityService

def test_eligibility_age_and_foir():
    birth_date = date(1995, 1, 1)
    monthly_income = Decimal("80000")
    obligations = Decimal("10000")
    amount = Decimal("200000")
    tenure = 24
    rate = Decimal("10.0")

    result = EligibilityService.evaluate(
        birth_date=birth_date,
        monthly_income=monthly_income,
        existing_obligations=obligations,
        requested_amount=amount,
        tenure_months=tenure,
        interest_rate=rate
    )
    assert result["is_eligible"] is True
    assert result["foir"] < Decimal("0.55")
