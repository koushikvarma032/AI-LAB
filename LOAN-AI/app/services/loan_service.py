from app.models.loan import LoanStatus, LoanApplication, LoanStatusHistory
from app.utils.extensions import db

class LoanStateMachine:
    VALID_TRANSITIONS = {
        LoanStatus.SUBMITTED: [LoanStatus.UNDER_REVIEW, LoanStatus.REJECTED],
        LoanStatus.UNDER_REVIEW: [LoanStatus.DOCUMENT_VERIFICATION, LoanStatus.REJECTED],
        LoanStatus.DOCUMENT_VERIFICATION: [LoanStatus.ELIGIBILITY_CHECK, LoanStatus.REJECTED],
        LoanStatus.ELIGIBILITY_CHECK: [LoanStatus.APPROVED, LoanStatus.REJECTED],
        LoanStatus.APPROVED: [LoanStatus.SANCTIONED, LoanStatus.REJECTED],
        LoanStatus.SANCTIONED: [LoanStatus.DISBURSED],
        LoanStatus.DISBURSED: [LoanStatus.ACTIVE],
        LoanStatus.ACTIVE: [LoanStatus.REPAYMENT, LoanStatus.CLOSED],
        LoanStatus.REPAYMENT: [LoanStatus.CLOSED],
        LoanStatus.CLOSED: [],
        LoanStatus.REJECTED: [],
    }

    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(from_status, [])
        return to_status in allowed

    @classmethod
    def transition(cls, application: LoanApplication, to_status: str, user_id=None, comment=None) -> LoanApplication:
        if not cls.can_transition(application.status, to_status):
            raise ValueError(f"Invalid state transition from '{application.status}' to '{to_status}'")
        
        from_status = application.status
        application.status = to_status
        
        history = LoanStatusHistory(
            loan_application_id=application.id,
            from_status=from_status,
            to_status=to_status,
            changed_by_user_id=user_id,
            comment=comment
        )
        db.session.add(history)
        db.session.commit()
        return application
