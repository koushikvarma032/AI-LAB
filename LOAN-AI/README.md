# LoanHub - Digital Lending & Loan Portfolio Platform

LoanHub is a digital lending and loan portfolio management platform featuring a Flask application architecture, credit assessment tools, and decimal-accurate financial calculations.

## Architectural Features

- **State Machine Loan Lifecycle**: Applications follow sequential status milestones:
  `SUBMITTED -> UNDER_REVIEW -> DOCUMENT_VERIFICATION -> ELIGIBILITY_CHECK -> APPROVED/REJECTED -> SANCTIONED -> DISBURSED -> ACTIVE -> REPAYMENT -> CLOSED`.
- **Credit Assessment**: Automated FOIR (Fixed Obligation to Income Ratio) calculation and age/income verification.
- **Decimal-Safe EMI Engine**: Python `Decimal` computations for amortization and zero-interest options.
- **Document Management**: File upload validation with MIME and size constraints.
- **Role-Based Access Control**: Separate customer and administrative operations.

## Project Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Seed the database:
   ```bash
   python -m scripts.seed
   ```

3. Launch application:
   ```bash
   python run.py
   ```

4. Run tests:
   ```bash
   pytest
   ```
