from decimal import Decimal
from app.services.emi_service import EMIService

def test_emi_calculation_standard():
    principal = Decimal("100000")
    rate = Decimal("12.0")
    tenure = 12
    emi = EMIService.calculate_monthly_emi(principal, rate, tenure)
    # Expected EMI for 100k at 12% for 12 months is ~8884.88
    assert emi == Decimal("8884.88")

def test_zero_interest_promotional():
    principal = Decimal("120000")
    rate = Decimal("0.0")
    tenure = 12
    emi = EMIService.calculate_monthly_emi(principal, rate, tenure)
    assert emi == Decimal("10000.00")
