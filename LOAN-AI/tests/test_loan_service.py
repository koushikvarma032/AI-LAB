from app.services.loan_service import LoanStateMachine
from app.models.loan import LoanStatus

def test_state_machine_valid_transitions():
    assert LoanStateMachine.can_transition(LoanStatus.SUBMITTED, LoanStatus.UNDER_REVIEW) is True
    assert LoanStateMachine.can_transition(LoanStatus.UNDER_REVIEW, LoanStatus.DOCUMENT_VERIFICATION) is True
    assert LoanStateMachine.can_transition(LoanStatus.DOCUMENT_VERIFICATION, LoanStatus.ELIGIBILITY_CHECK) is True
    assert LoanStateMachine.can_transition(LoanStatus.ELIGIBILITY_CHECK, LoanStatus.APPROVED) is True
    assert LoanStateMachine.can_transition(LoanStatus.APPROVED, LoanStatus.SANCTIONED) is True
    assert LoanStateMachine.can_transition(LoanStatus.SANCTIONED, LoanStatus.DISBURSED) is True
    assert LoanStateMachine.can_transition(LoanStatus.DISBURSED, LoanStatus.ACTIVE) is True
    assert LoanStateMachine.can_transition(LoanStatus.ACTIVE, LoanStatus.CLOSED) is True

def test_state_machine_invalid_transitions():
    assert LoanStateMachine.can_transition(LoanStatus.SUBMITTED, LoanStatus.DISBURSED) is False
    assert LoanStateMachine.can_transition(LoanStatus.CLOSED, LoanStatus.SUBMITTED) is False
