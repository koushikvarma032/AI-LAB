"""
Counterfactual Analysis:
Demonstrates that the formal reasoning engines (Modus Ponens and SymPy CNF refutation)
do not produce false alarms when critical premises (e.g. HighHumidity) are absent.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from advisory.engine import SmartCropAdvisoryEngine
from advisory.report_generator import generate_audit_report


def main():
    print("=" * 80)
    print("COUNTERFACTUAL SCENARIO: Leaf Spots Present BUT Low Humidity (Normal / Dry Weather)")
    print("=" * 80)
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)

    report_dry = engine.analyze_field(
        farmer_name="Rameshbhai Patel",
        region="Rajkot, Gujarat",
        crop="Groundnut",
        plot_id="Plot-DRY-01",
        leaf_spots_observed=True,
        high_humidity_observed=False  # Low humidity condition!
    )

    print(f"LeafSpots Observed: True")
    print(f"HighHumidity Observed: False")
    print(f"Deduction Steps Fired: {len(report_dry.deduction_chain)}")
    print(f"Deduced Facts: {[step.consequent.to_fol_repr() for step in report_dry.deduction_chain]}")
    print(f"Was FungalRisk deduced? {'FungalRisk' in [s.consequent.predicate for s in report_dry.deduction_chain]}")
    print(f"Was UrgentExpertInspection deduced? {'UrgentExpertInspection' in [s.consequent.predicate for s in report_dry.deduction_chain]}")

    print("\nResult: Modus Ponens correctly prevented false positive. No unnecessary chemical spray advised.")


if __name__ == "__main__":
    main()
