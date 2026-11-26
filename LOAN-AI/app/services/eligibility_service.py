from decimal import Decimal
from datetime import date
from app.services.emi_service import EMIService

class EligibilityService:
    MIN_AGE = 21
    MAX_AGE = 65
    MIN_MONTHLY_INCOME = Decimal("15000.00")
    MAX_FOIR = Decimal("0.55")  # Fixed Obligation to Income Ratio 55%

    @classmethod
    def evaluate(
        cls,
        birth_date: date,
        monthly_income: Decimal,
        existing_obligations: Decimal,
        requested_amount: Decimal,
        tenure_months: int,
        interest_rate: Decimal
    ) -> dict:
        results = {
            "is_eligible": True,
            "reasons": [],
            "foir": Decimal("0.00"),
            "max_eligible_emi": Decimal("0.00"),
            "proposed_emi": Decimal("0.00"),
        }

        # Age verification
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < cls.MIN_AGE:
                results["is_eligible"] = False
                results["reasons"].append(f"Applicant age ({age}) is below minimum required age of {cls.MIN_AGE}.")
            if age > cls.MAX_AGE:
                results["is_eligible"] = False
                results["reasons"].append(f"Applicant age ({age}) exceeds maximum allowed age of {cls.MAX_AGE}.")
        else:
            results["is_eligible"] = False
            results["reasons"].append("Applicant date of birth not provided.")

        monthly_income = Decimal(str(monthly_income or "0"))
        existing_obligations = Decimal(str(existing_obligations or "0"))

        if monthly_income < cls.MIN_MONTHLY_INCOME:
            results["is_eligible"] = False
            results["reasons"].append(f"Monthly income ({monthly_income}) is below minimum threshold of {cls.MIN_MONTHLY_INCOME}.")

        # Proposed EMI calculation
        try:
            proposed_emi = EMIService.calculate_monthly_emi(requested_amount, interest_rate, tenure_months)
            results["proposed_emi"] = proposed_emi
        except Exception as e:
            results["is_eligible"] = False
            results["reasons"].append(f"Could not compute EMI: {str(e)}")
            return results

        # FOIR calculation: (Existing obligations + proposed EMI) / Monthly income
        if monthly_income > Decimal("0"):
            total_obligation = existing_obligations + proposed_emi
            foir = total_obligation / monthly_income
            results["foir"] = foir.quantize(Decimal("0.0001"))
            results["max_eligible_emi"] = (monthly_income * cls.MAX_FOIR - existing_obligations).quantize(Decimal("0.01"))

            if foir > cls.MAX_FOIR:
                results["is_eligible"] = False
                results["reasons"].append(
                    f"Fixed Obligation to Income Ratio ({foir * Decimal('100'):.1f}%) exceeds maximum limit of {cls.MAX_FOIR * Decimal('100'):.1f}%."
                )

        return results
