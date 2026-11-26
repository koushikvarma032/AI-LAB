"""Development database seeder for LoanHub."""
from decimal import Decimal
from datetime import date
from app import create_app
from app.utils.extensions import db
from app.models.user import User
from app.models.loan import LoanType

def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Create Admin
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                email="admin@loanhub.internal",
                first_name="Operations",
                last_name="Manager",
                role="admin"
            )
            admin.set_password("admin123")
            db.session.add(admin)

        # Create Demo Customer
        if not User.query.filter_by(username="customer").first():
            customer = User(
                username="customer",
                email="customer@loanhub.internal",
                first_name="Aarav",
                last_name="Patel",
                role="customer",
                pan_number="ABCDE1234F",
                aadhaar_number="123456789012",
                date_of_birth=date(1992, 7, 10),
                monthly_income=Decimal("75000.00"),
                current_obligations=Decimal("12000.00"),
            )
            customer.set_password("customer123")
            db.session.add(customer)

        # Create Loan Types
        types_data = [
            {
                "code": "PERSONAL",
                "name": "Personal Loan",
                "description": "Flexible multi-purpose financing with rapid credit evaluation.",
                "min_amount": Decimal("25000"),
                "max_amount": Decimal("1500000"),
                "min_tenure_months": 6,
                "max_tenure_months": 60,
                "base_interest_rate": Decimal("11.50")
            },
            {
                "code": "HOME",
                "name": "Home Construction & Purchase",
                "description": "Long-term mortgage financing for residential properties.",
                "min_amount": Decimal("500000"),
                "max_amount": Decimal("10000000"),
                "min_tenure_months": 12,
                "max_tenure_months": 360,
                "base_interest_rate": Decimal("8.40")
            },
            {
                "code": "BUSINESS",
                "name": "SME Working Capital",
                "description": "Growth capital and equipment financing for registered businesses.",
                "min_amount": Decimal("100000"),
                "max_amount": Decimal("5000000"),
                "min_tenure_months": 12,
                "max_tenure_months": 84,
                "base_interest_rate": Decimal("12.75")
            },
            {
                "code": "EDUCATION",
                "name": "Higher Education Scheme",
                "description": "Specialized financing for premier domestic and international studies.",
                "min_amount": Decimal("100000"),
                "max_amount": Decimal("4000000"),
                "min_tenure_months": 12,
                "max_tenure_months": 120,
                "base_interest_rate": Decimal("7.85")
            }
        ]

        for item in types_data:
            existing = LoanType.query.filter_by(code=item["code"]).first()
            if not existing:
                loan_type = LoanType(**item)
                db.session.add(loan_type)

        db.session.commit()
        print("Database seeded with default schemes and demo users successfully.")

if __name__ == "__main__":
    seed_database()
