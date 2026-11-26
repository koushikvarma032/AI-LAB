"""
Audit report generator for terminal printing and markdown generation.
Provides human-readable, auditable traces of both Modus Ponens deduction
and SymPy CNF resolution refutation proofs.
"""

from typing import List
from tabulate import tabulate
from .models import AdvisoryReport, DeductionStep, RefutationProofResult


def generate_audit_report(report: AdvisoryReport) -> str:
    """
    Renders an auditable text report suitable for agronomic auditors, extension scientists, and terminal inspection.
    """
    lines = []
    w = 88
    lines.append("=" * w)
    lines.append("  SMART CROP DISEASE ADVISORY SYSTEM - FORMAL INFERENCE AUDIT REPORT")
    lines.append("  Domain: Cotton & Groundnut Pathology | Region: Gujarat, India")
    lines.append("=" * w)
    lines.append(f"  Farmer: {report.farmer_name} | Plot ID: {report.plot_id}")
    lines.append(f"  Crop: {report.crop} | Agro-Climatic Zone: {report.region}")
    lines.append(f"  Report Generated: {report.generated_at}")
    lines.append("-" * w)

    # 1. Input Facts
    lines.append("\n[1] INITIAL OBSERVED FACTS & SENSOR TELEMETRY:")
    fact_table = [
        [idx, f.to_fol_repr(), f.source, f.timestamp]
        for idx, f in enumerate(report.observed_facts, 1)
    ]
    lines.append(tabulate(fact_table, headers=["#", "Atomic Fact (FOL)", "Source Evidence", "Timestamp"], tablefmt="grid"))

    # 2. Modus Ponens Deduction Chain
    lines.append("\n" + "=" * w)
    lines.append("  [2] AUDITABLE MODUS PONENS DEDUCTION CHAIN")
    lines.append("=" * w)
    lines.append("Formal Rule of Inference Applied:  P ,  P -> Q  |-  Q\n")

    for step in report.deduction_chain:
        lines.append(f"--- [STEP {step.step_num}] Rule Fired: [{step.rule_id}] {step.rule_name} ---")
        lines.append(f"  Antecedents Satisfied : {', '.join([p.to_fol_repr() for p in step.premises])}")
        lines.append(f"  Deduced Consequent    : {step.consequent.to_fol_repr()}")
        lines.append(f"  Formal Schema         :")
        for schema_line in step.formal_modus_ponens.split("\n"):
            lines.append(f"    {schema_line}")
        lines.append(f"  Agronomic Rationale   : {step.rationale}")
        lines.append(f"  Audit Timestamp       : {step.timestamp}")
        lines.append("")

    # 3. SymPy CNF Resolution Refutation Proofs
    lines.append("=" * w)
    lines.append("  [3] SymPy CNF RESOLUTION REFUTATION PROOFS")
    lines.append("=" * w)
    lines.append("Mathematical Foundation: KB |= Q  <=>  (KB ^ ~Q) is UNSATISFIABLE (Derives [] / Contradiction)\n")

    for query_name, proof in report.refutation_proofs.items():
        lines.append(f"--- THEOREM PROVING FOR: {proof.query_fol} ---")
        lines.append(f"  Proof Verdict            : {'PROVED (VALID THEOREM)' if proof.is_proved else 'UNPROVEN'}")
        lines.append(f"  SymPy SAT Status         : {proof.sympy_verification_status}")
        lines.append(f"  Proof Computation Time   : {proof.proof_time_ms} ms")
        lines.append(f"  Negated Query Clause     : {proof.negated_query_clause[0]} : {proof.negated_query_clause[1]}")
        lines.append("\n  Initial CNF Clauses Pool (KB + ~Goal):")

        init_table = [[cid, expr] for cid, expr in proof.initial_clauses]
        lines.append(tabulate(init_table, headers=["Clause ID", "CNF Disjunction (Literals)"], tablefmt="simple"))

        lines.append("\n  Step-by-Step Resolution Refutation Steps:")
        res_table = [
            [
                s.step_num,
                f"{s.clause1_id} + {s.clause2_id}",
                s.resolved_literal,
                s.resolvent_id,
                s.resolvent_str,
                "CONTRADICTION []" if s.is_contradiction else "Valid Resolvent"
            ]
            for s in proof.resolution_steps
        ]
        lines.append(tabulate(
            res_table,
            headers=["#", "Parent Clauses", "Resolved On", "Resolvent ID", "Resolvent Clause", "Status"],
            tablefmt="grid"
        ))

        if proof.is_proved:
            lines.append(f"\n  >> Q.E.D. Empty clause [] derived at resolution step. Hypothesis ~{proof.query_fol} is REFUTED.")
            lines.append(f"  >> Conclusion: {proof.query_fol} is a sound logical consequence of the Knowledge Base.")
        lines.append("\n" + "-" * w)

    # 4. Actionable Agronomic Advisories
    lines.append("\n" + "=" * w)
    lines.append("  [4] ACTIONABLE FIELD ADVISORY & INTERVENTION PROTOCOL")
    lines.append("=" * w)
    adv_table = [
        [item.urgency, item.category, item.recommendation, item.scientific_basis]
        for item in report.advisories
    ]
    lines.append(tabulate(adv_table, headers=["Urgency", "Category", "Recommended Intervention", "Scientific Rationale"], tablefmt="grid"))
    lines.append("=" * w)

    return "\n".join(lines)


def export_markdown_report(report: AdvisoryReport, filepath: str):
    """Exports full audit report as a clean GitHub-flavored markdown document."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Smart Crop Disease Advisory Report\n\n")
        f.write(f"- **Farmer:** {report.farmer_name}\n")
        f.write(f"- **Region:** {report.region}\n")
        f.write(f"- **Crop:** {report.crop}\n")
        f.write(f"- **Plot:** {report.plot_id}\n")
        f.write(f"- **Generated At:** {report.generated_at}\n\n")

        f.write("## 1. Observed Evidence\n\n")
        f.write("| # | Fact (FOL) | Source | Timestamp |\n")
        f.write("|---|---|---|---|\n")
        for i, fact in enumerate(report.observed_facts, 1):
            f.write(f"| {i} | `{fact.to_fol_repr()}` | {fact.source} | {fact.timestamp} |\n")

        f.write("\n## 2. Auditable Modus Ponens Deduction Chain\n\n")
        for step in report.deduction_chain:
            f.write(f"### Step {step.step_num}: Rule `{step.rule_id}` - {step.rule_name}\n\n")
            f.write(f"- **Antecedents:** `{', '.join([p.to_fol_repr() for p in step.premises])}`\n")
            f.write(f"- **Consequent:** `{step.consequent.to_fol_repr()}`\n")
            f.write("```text\n")
            f.write(step.formal_modus_ponens + "\n")
            f.write("```\n")
            f.write(f"- **Rationale:** {step.rationale}\n\n")

        f.write("## 3. SymPy CNF Refutation Proofs\n\n")
        for query_name, proof in report.refutation_proofs.items():
            f.write(f"### Query: `{proof.query_fol}`\n\n")
            f.write(f"- **Verdict:** **{'PROVED (VALID)' if proof.is_proved else 'UNPROVEN'}**\n")
            f.write(f"- **SymPy SAT Solver:** {proof.sympy_verification_status}\n")
            f.write(f"- **Computation Time:** {proof.proof_time_ms} ms\n\n")

            f.write("#### Step-by-Step Resolution Refutation\n\n")
            f.write("| Step | Parents | Resolved Literal | Resolvent ID | Resolvent Clause | Status |\n")
            f.write("|---|---|---|---|---|---|\n")
            for s in proof.resolution_steps:
                stat = r"**Contradiction ($\square$)**" if s.is_contradiction else "Resolvent"
                f.write(f"| {s.step_num} | {s.clause1_id} + {s.clause2_id} | `{s.resolved_literal}` | {s.resolvent_id} | `{s.resolvent_str}` | {stat} |\n")
            f.write("\n")

        f.write("## 4. Agronomic Advisories\n\n")
        f.write("| Urgency | Category | Action | Basis |\n")
        f.write("|---|---|---|---|\n")
        for item in report.advisories:
            f.write(f"| **{item.urgency}** | {item.category} | {item.recommendation} | {item.scientific_basis} |\n")
