"""
Main CLI entrypoint for Smart Crop Disease Advisory AI System.
Demonstrates the Gujarat Farmer Crop Disease Advisory:
  - Farmer in Gujarat notices leaf spots and high humidity.
  - R2: (LeafSpots(x) AND HighHumidity(x)) -> FungalRisk(x)
  - R3: Flags Urgent Expert Inspection
  - Auditable Modus Ponens deduction chain
  - SymPy CNF refutation proof
"""

import sys
import argparse
from advisory.engine import SmartCropAdvisoryEngine
from advisory.report_generator import generate_audit_report, export_markdown_report


def run_gujarat_case_study():
    print("\n" + "=" * 90)
    print("   SMART CROP DISEASE ADVISORY AI SYSTEM (COTTON & GROUNDNUT - GUJARAT)")
    print("   Formal Automated Deduction & Refutation Proof Engine")
    print("=" * 90)

    engine = SmartCropAdvisoryEngine(use_extended_rules=True)

    # -------------------------------------------------------------
    # CASE STUDY 1: Groundnut Farmer in Rajkot / Junagadh, Gujarat
    # -------------------------------------------------------------
    print("\n>>> RUNNING CASE STUDY 1: Groundnut (Tikka Disease Epiphytotic Risk)")
    report_groundnut = engine.analyze_field(
        farmer_name="Rameshbhai Patel",
        region="Saurashtra (Rajkot / Junagadh), Gujarat",
        crop="Groundnut (Arachis hypogaea / GG-20)",
        plot_id="Plot-GJ-GND-101",
        leaf_spots_observed=True,
        high_humidity_observed=True,
        soil_moisture_high=True
    )
    print(generate_audit_report(report_groundnut))
    export_markdown_report(report_groundnut, "audit_report_groundnut.md")
    print("\n[+] Full Groundnut audit report successfully saved to 'audit_report_groundnut.md'")

    # -------------------------------------------------------------
    # CASE STUDY 2: Cotton Farmer in Surendranagar / Vadodara, Gujarat
    # -------------------------------------------------------------
    print("\n>>> RUNNING CASE STUDY 2: Bt-Cotton (Alternaria / Cercospora Risk)")
    report_cotton = engine.analyze_field(
        farmer_name="Bharatbhai Desai",
        region="Surendranagar / Central Gujarat",
        crop="Bt-Cotton (Gossypium hirsutum / Hybrid-6)",
        plot_id="Plot-GJ-COT-204",
        leaf_spots_observed=True,
        high_humidity_observed=True,
        soil_moisture_high=True
    )
    print(generate_audit_report(report_cotton))
    export_markdown_report(report_cotton, "audit_report_cotton.md")
    print("\n[+] Full Cotton audit report successfully saved to 'audit_report_cotton.md'")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Crop Disease Advisory AI System for Cotton & Groundnut (Gujarat)"
    )
    parser.add_argument("--farmer", type=str, default="Rameshbhai Patel", help="Farmer Name")
    parser.add_argument("--region", type=str, default="Rajkot, Gujarat", help="Region / Agro-Climatic Zone")
    parser.add_argument("--crop", type=str, default="Groundnut", choices=["Groundnut", "Cotton"], help="Crop type")
    parser.add_argument("--plot", type=str, default="Plot-GJ-01", help="Plot Identifier")
    parser.add_argument("--leaf-spots", action="store_true", default=True, help="Leaf spots observed")
    parser.add_argument("--high-humidity", action="store_true", default=True, help="High humidity (>80%) observed")
    parser.add_argument("--demo-all", action="store_true", default=True, help="Run both Gujarat case studies")

    args = parser.parse_args()

    if args.demo_all:
        run_gujarat_case_study()
    else:
        engine = SmartCropAdvisoryEngine(use_extended_rules=True)
        report = engine.analyze_field(
            farmer_name=args.farmer,
            region=args.region,
            crop=args.crop,
            plot_id=args.plot,
            leaf_spots_observed=args.leaf_spots,
            high_humidity_observed=args.high_humidity
        )
        print(generate_audit_report(report))


if __name__ == "__main__":
    main()
