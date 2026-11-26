"""
Standalone demonstration: Gujarat Groundnut Tikka Disease advisory and formal proofs.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from advisory.engine import SmartCropAdvisoryEngine
from advisory.report_generator import generate_audit_report


def main():
    print("Executing Gujarat Groundnut Case Study...")
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)
    report = engine.analyze_field(
        farmer_name="Kishorbhai Radadiya",
        region="Junagadh, Saurashtra, Gujarat",
        crop="Groundnut (Arachis hypogaea / GJG-22)",
        plot_id="Field-JAU-GN-88",
        leaf_spots_observed=True,
        high_humidity_observed=True
    )
    print(generate_audit_report(report))


if __name__ == "__main__":
    main()
