"""
Smart Crop Disease Advisory System for Cotton & Groundnut.
Formal AI Reasoning Engine using Auditable Modus Ponens and SymPy CNF Refutation Proofs.
"""

from .models import Fact, Rule, DeductionStep, ResolutionStep, RefutationProofResult, AdvisoryReport
from .knowledge_base import AgriculturalKnowledgeBase, get_gujarat_crop_profile
from .modus_ponens import ModusPonensDeductionEngine
from .cnf_refutation import SymPyCNFRefutationEngine
from .engine import SmartCropAdvisoryEngine
from .report_generator import generate_audit_report

__all__ = [
    "Fact",
    "Rule",
    "DeductionStep",
    "ResolutionStep",
    "RefutationProofResult",
    "AdvisoryReport",
    "AgriculturalKnowledgeBase",
    "get_gujarat_crop_profile",
    "ModusPonensDeductionEngine",
    "SymPyCNFRefutationEngine",
    "SmartCropAdvisoryEngine",
    "generate_audit_report",
]
