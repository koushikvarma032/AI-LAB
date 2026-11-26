"""
Data models and structure definitions for formal inference and advisory reporting.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Set, Tuple


@dataclass(frozen=True)
class Fact:
    """Represents an atomic ground fact in the agricultural domain."""
    predicate: str
    target: str
    value: bool = True
    source: str = "Observation"
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def to_symbol_name(self) -> str:
        """Normalized propositional symbol representation: e.g. LeafSpots_plot1"""
        clean_target = self.target.replace("-", "_").replace(" ", "_")
        return f"{self.predicate}_{clean_target}"

    def to_fol_repr(self) -> str:
        """First-order notation: e.g. LeafSpots(plot1)"""
        return f"{self.predicate}({self.target})"

    def __str__(self) -> str:
        return self.to_fol_repr() if self.value else f"~{self.to_fol_repr()}"


@dataclass
class Rule:
    """Represents an agronomic formal implication rule: Antecedent -> Consequent."""
    rule_id: str
    name: str
    antecedents: List[str]  # e.g. ["LeafSpots", "HighHumidity"]
    consequent: str         # e.g. "FungalRisk"
    description: str
    agronomic_rationale: str
    source_reference: str = "ICAR / Gujarat Agricultural University (AAU/JAU) Extension Guidelines"

    def get_formal_formula(self, target: str) -> str:
        """Returns FOL formula: (Antecedent1(x) AND Antecedent2(x)) -> Consequent(x)"""
        ant_str = " AND ".join(f"{ant}({target})" for ant in self.antecedents)
        if len(self.antecedents) > 1:
            ant_str = f"({ant_str})"
        return f"{ant_str} -> {self.consequent}({target})"


@dataclass
class DeductionStep:
    """Represents a discrete, auditable step in the Modus Ponens deduction chain."""
    step_num: int
    rule_id: str
    rule_name: str
    premises: List[Fact]
    consequent: Fact
    formal_modus_ponens: str  # e.g. "From P & Q and (P & Q -> R), deduce R"
    rationale: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class ResolutionStep:
    """Represents an atomic propositional resolution refutation step."""
    step_num: int
    clause1_id: str
    clause1_str: str
    clause2_id: str
    clause2_str: str
    resolved_literal: str
    resolvent_id: str
    resolvent_str: str
    is_contradiction: bool = False


@dataclass
class RefutationProofResult:
    """Result of a SymPy-backed CNF resolution refutation theorem proving."""
    query_symbol: str
    query_fol: str
    is_proved: bool
    initial_clauses: List[Tuple[str, str]]  # list of (clause_id, clause_str)
    negated_query_clause: Tuple[str, str]
    resolution_steps: List[ResolutionStep]
    satisfiable_under_negation: bool  # False means KB & ~Q is unsatisfiable -> proved
    sympy_verification_status: str
    proof_time_ms: float


@dataclass
class AgronomicAdvisoryItem:
    """Structured agronomic recommendation based on deduced risk."""
    category: str  # Immediate Action, Chemical, Cultural, Telemetry
    recommendation: str
    urgency: str   # CRITICAL, HIGH, MEDIUM, LOW
    scientific_basis: str


@dataclass
class AdvisoryReport:
    """Full comprehensive report containing facts, audit chain, refutation proof, and advisory."""
    farmer_name: str
    region: str
    crop: str
    plot_id: str
    observed_facts: List[Fact]
    deduction_chain: List[DeductionStep]
    refutation_proofs: Dict[str, RefutationProofResult]
    advisories: List[AgronomicAdvisoryItem]
    generated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
