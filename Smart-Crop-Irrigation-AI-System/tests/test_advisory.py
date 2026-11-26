"""
Unit & Integration Tests for Smart Crop Disease Advisory AI System.
Tests Modus Ponens forward deduction, SymPy CNF resolution refutation theorem proving,
and Gujarat crop pathology advisories for Cotton and Groundnut.
"""

import pytest
from advisory.models import Fact, Rule
from advisory.knowledge_base import AgriculturalKnowledgeBase, get_gujarat_crop_profile
from advisory.modus_ponens import ModusPonensDeductionEngine
from advisory.cnf_refutation import SymPyCNFRefutationEngine
from advisory.engine import SmartCropAdvisoryEngine
from advisory.report_generator import generate_audit_report


def test_rule_r2_modus_ponens_deduction():
    """Verify Rule R2: (LeafSpots(x) AND HighHumidity(x)) -> FungalRisk(x)."""
    kb = AgriculturalKnowledgeBase(use_extended_rules=False)
    engine = ModusPonensDeductionEngine(kb)

    facts = [
        Fact("LeafSpots", "plot_alpha"),
        Fact("HighHumidity", "plot_alpha")
    ]
    deduced_facts, chain = engine.infer(facts, "plot_alpha")
    predicates = [f.predicate for f in deduced_facts]

    assert "FungalRisk" in predicates
    assert len(chain) >= 1

    # Check R2 step specifically
    r2_step = next(s for s in chain if s.rule_id == "R2")
    assert r2_step.consequent.predicate == "FungalRisk"
    assert len(r2_step.premises) == 2
    assert {p.predicate for p in r2_step.premises} == {"LeafSpots", "HighHumidity"}


def test_rule_r3_urgent_inspection_flag():
    """Verify Rule R3 triggers UrgentExpertInspection upon FungalRisk."""
    kb = AgriculturalKnowledgeBase(use_extended_rules=False)
    engine = ModusPonensDeductionEngine(kb)

    facts = [
        Fact("LeafSpots", "plot_beta"),
        Fact("HighHumidity", "plot_beta")
    ]
    deduced_facts, chain = engine.infer(facts, "plot_beta")
    predicates = [f.predicate for f in deduced_facts]

    assert "UrgentExpertInspection" in predicates
    r3_step = next(s for s in chain if s.rule_id == "R3")
    assert r3_step.consequent.predicate == "UrgentExpertInspection"


def test_sympy_cnf_refutation_fungal_risk():
    """Verify SymPy CNF refutation formally proves FungalRisk and derives contradiction."""
    kb = AgriculturalKnowledgeBase(use_extended_rules=False)
    cnf_engine = SymPyCNFRefutationEngine()

    facts = [
        Fact("LeafSpots", "plot_test"),
        Fact("HighHumidity", "plot_test")
    ]

    result = cnf_engine.prove(
        rules=kb.rules,
        facts=facts,
        query_predicate="FungalRisk",
        target="plot_test"
    )

    assert result.is_proved is True
    assert result.satisfiable_under_negation is False
    assert len(result.resolution_steps) > 0
    # Last step should be empty clause / contradiction
    assert result.resolution_steps[-1].is_contradiction is True


def test_sympy_cnf_refutation_urgent_inspection():
    """Verify SymPy CNF refutation formally proves UrgentExpertInspection."""
    kb = AgriculturalKnowledgeBase(use_extended_rules=False)
    cnf_engine = SymPyCNFRefutationEngine()

    facts = [
        Fact("LeafSpots", "plot_test"),
        Fact("HighHumidity", "plot_test")
    ]

    result = cnf_engine.prove(
        rules=kb.rules,
        facts=facts,
        query_predicate="UrgentExpertInspection",
        target="plot_test"
    )

    assert result.is_proved is True
    assert result.satisfiable_under_negation is False
    assert result.resolution_steps[-1].is_contradiction is True


def test_counterfactual_missing_humidity_no_false_positive():
    """Verify that when humidity is normal/low, FungalRisk is NOT deduced."""
    kb = AgriculturalKnowledgeBase(use_extended_rules=True)
    engine = ModusPonensDeductionEngine(kb)

    # Leaf spots present, but humidity NOT high
    facts = [
        Fact("LeafSpots", "dry_plot"),
        Fact("VulnerableCrop", "dry_plot"),
        Fact("LocationGujarat", "dry_plot")
    ]
    deduced_facts, chain = engine.infer(facts, "dry_plot")
    predicates = [f.predicate for f in deduced_facts]

    assert "FungalRisk" not in predicates
    assert "UrgentExpertInspection" not in predicates


def test_cotton_gujarat_full_pipeline():
    """Verify complete pipeline for a Cotton farmer in Gujarat."""
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)
    report = engine.analyze_field(
        farmer_name="Sureshbhai",
        region="Surendranagar, Gujarat",
        crop="Cotton",
        plot_id="COT-GJ-01",
        leaf_spots_observed=True,
        high_humidity_observed=True
    )

    assert len(report.deduction_chain) >= 3
    assert "FungalRisk" in report.refutation_proofs
    assert report.refutation_proofs["FungalRisk"].is_proved is True
    assert "UrgentExpertInspection" in report.refutation_proofs
    assert report.refutation_proofs["UrgentExpertInspection"].is_proved is True

    # Check advisory items
    urgencies = [item.urgency for item in report.advisories]
    assert "CRITICAL" in urgencies
    assert "HIGH" in urgencies


def test_groundnut_gujarat_full_pipeline():
    """Verify complete pipeline for a Groundnut farmer in Gujarat."""
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)
    report = engine.analyze_field(
        farmer_name="Manishbhai",
        region="Junagadh, Gujarat",
        crop="Groundnut",
        plot_id="GND-GJ-99",
        leaf_spots_observed=True,
        high_humidity_observed=True
    )

    assert report.crop == "Groundnut"
    assert any("WITHHOLD OVERHEAD SPRINKLER IRRIGATION" in a.recommendation for a in report.advisories)
    assert any("Tikka" in a.scientific_basis or "Cercospora" in a.scientific_basis for a in report.advisories)


def test_audit_report_generation_text():
    """Verify formatting of the generated human-readable audit report."""
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)
    report = engine.analyze_field(
        farmer_name="Rameshbhai Patel",
        region="Rajkot, Gujarat",
        crop="Groundnut",
        plot_id="Plot-Test",
        leaf_spots_observed=True,
        high_humidity_observed=True
    )
    rendered = generate_audit_report(report)
    assert "AUDITABLE MODUS PONENS DEDUCTION CHAIN" in rendered
    assert "SymPy CNF RESOLUTION REFUTATION PROOFS" in rendered
    assert "R2" in rendered
    assert "R3" in rendered
    assert "CONTRADICTION" in rendered
