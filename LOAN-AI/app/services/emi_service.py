from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from dateutil.relativedelta import relativedelta

TWO_PLACES = Decimal("0.01")

class EMIService:
    @staticmethod
    def calculate_monthly_emi(principal: Decimal, annual_interest_rate: Decimal, tenure_months: int) -> Decimal:
        principal = Decimal(str(principal))
        rate = Decimal(str(annual_interest_rate))
        n = int(tenure_months)

        if n <= 0:
            raise ValueError("Tenure months must be positive")
        if principal <= 0:
            raise ValueError("Principal must be positive")

        # Zero interest promotional program
        if rate == Decimal("0"):
            emi = principal / Decimal(str(n))
            return emi.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

        monthly_r = rate / Decimal("1200")
        factor = (Decimal("1") + monthly_r) ** n
        emi = (principal * monthly_r * factor) / (factor - Decimal("1"))
        return emi.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

    @classmethod
    def generate_amortization_schedule(
        cls,
        principal: Decimal,
        annual_interest_rate: Decimal,
        tenure_months: int,
        start_date: date = None
    ) -> list[dict]:
        if start_date is None:
            start_date = date.today()

        principal = Decimal(str(principal))
        rate = Decimal(str(annual_interest_rate))
        tenure = int(tenure_months)
        monthly_emi = cls.calculate_monthly_emi(principal, rate, tenure)
        monthly_r = rate / Decimal("1200")

        schedule = []
        current_balance = principal

        for i in range(1, tenure + 1):
            installment_date = start_date + relativedelta(months=i)
            opening = current_balance

            if rate == Decimal("0"):
                interest = Decimal("0.00")
            else:
                interest = (opening * monthly_r).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

            principal_comp = monthly_emi - interest

            # Final month rounding adjustment
            if i == tenure or opening < principal_comp:
                principal_comp = opening
                monthly_emi = principal_comp + interest
                closing = Decimal("0.00")
            else:
                closing = opening - principal_comp

            schedule.append({
                "installment_number": i,
                "due_date": installment_date,
                "opening_balance": opening,
                "principal_component": principal_comp,
                "interest_component": interest,
                "total_installment": monthly_emi,
                "closing_balance": closing,
            })
            current_balance = closing

        return schedule
