"""
Standalone demonstration: Gujarat Cotton Alternaria / Blight disease advisory and formal proofs.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from advisory.engine import SmartCropAdvisoryEngine
from advisory.report_generator import generate_audit_report


def main():
    print("Executing Gujarat Cotton Case Study...")
    engine = SmartCropAdvisoryEngine(use_extended_rules=True)
    report = engine.analyze_field(
        farmer_name="Govindbhai Patel",
        region="Surendranagar, Gujarat",
        crop="Cotton (Bt-Cotton / Hybrid)",
        plot_id="Field-COT-SRN-12",
        leaf_spots_observed=True,
        high_humidity_observed=True
    )
    print(generate_audit_report(report))


if __name__ == "__main__":
    main()
