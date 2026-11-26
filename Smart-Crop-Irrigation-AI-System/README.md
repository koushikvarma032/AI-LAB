# Smart Crop Disease Advisory AI System (Cotton & Groundnut - Gujarat)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![SymPy Logic Engine](https://img.shields.io/badge/SymPy-1.14.0-darkgreen.svg)](https://www.sympy.org/)
[![Formal Reasoning](https://img.shields.io/badge/Deduction-Modus%20Ponens%20%26%20CNF%20Refutation-orange.svg)]()
[![Tests](https://img.shields.io/badge/pytest-8%20passed-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/AgroPathology-Gujarat%20Cotton%20%26%20Groundnut-purple.svg)]()

An automated agronomic AI reasoning engine designed for cash-crop smallholders in Gujarat, India (Cotton and Groundnut). When a farmer reports field observations—such as foliar leaf spots alongside elevated relative humidity—the system formally evaluates disease risk, alerts extension authorities, and issues precision irrigation and chemical advisories.

Crucially, **every conclusion is mathematically certified**:
1. **Forward Auditable Modus Ponens Deduction Chain**: An immutable, step-by-step audit trail showing exact ground premises, fired production rules, and intermediate conclusions.
2. **SymPy-Powered CNF Resolution Refutation Proof**: Converts all domain axioms into Conjunctive Normal Form (CNF) clauses, injects the negated goal hypothesis ($\neg \text{Goal}$), and derives the empty clause ($\square$ / Contradiction) via formal resolution theorem proving, independently cross-validated using SymPy's SAT solver.

---

## Table of Contents

- [Core Problem Statement](#core-problem-statement)
- [Gujarat Agricultural Context (Cotton & Groundnut)](#gujarat-agricultural-context-cotton--groundnut)
- [Formal Mathematical & Logical Foundations](#formal-mathematical--logical-foundations)
  - [1. Knowledge Base & Production Rules](#1-knowledge-base--production-rules)
  - [2. Auditable Modus Ponens Inference](#2-auditable-modus-ponens-inference)
  - [3. SymPy CNF Resolution Refutation Proof](#3-sympy-cnf-resolution-refutation-proof)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Execution & Audit Examples](#execution--audit-examples)
  - [Running the Main Advisory Case Studies](#running-the-main-advisory-case-studies)
  - [Modus Ponens Audit Trail Sample](#modus-ponens-audit-trail-sample)
  - [Resolution Refutation Proof Sample](#resolution-refutation-proof-sample)
  - [Actionable Agronomic Advisory](#actionable-agronomic-advisory)
- [Test Suite & Verification](#test-suite--verification)
- [Repository Structure](#repository-structure)
- [Agronomic References](#agronomic-references)

---

## Core Problem Statement

> **Scenario**: A farmer in Gujarat notices leaf spots and high ambient humidity. The AI engine applies:
> - **Rule R2**: $(\text{LeafSpots}(x) \land \text{HighHumidity}(x)) \implies \text{FungalRisk}(x)$, concluding **Fungal Disease Risk**.
> - **Rule R3**: Flags **Urgent Expert Inspection**.
> - **Advisory**: Restrict overhead sprinkler irrigation to curtail splash dispersal of spores and prepare targeted protective fungicides.
> - **Auditing**: Every conclusion must be backed by an auditable **Modus Ponens deduction chain** and a **SymPy CNF refutation proof**.

---

## Gujarat Agricultural Context (Cotton & Groundnut)

Gujarat is India's leading producer of both Cotton (*Kapas*) and Groundnut (*Magfali*), concentrated heavily in Saurashtra (Rajkot, Junagadh, Amreli, Jamnagar, Bhavnagar) and North/Central Gujarat (Surendranagar, Sabarkantha, Vadodara).

| Crop | High-Risk Pathogen Epiphytotics | Environmental Triggers | Urgent Agronomic Action |
|---|---|---|---|
| **Groundnut** (*Arachis hypogaea*) | **Tikka Disease** (Early Leaf Spot: *Cercospora arachidicola*; Late Leaf Spot: *Phaeoisariopsis personata*) | Relative Humidity $> 80\%$, Temperature $25^\circ\text{C} - 32^\circ\text{C}$, prolonged leaf wetness | Immediate field scouting by KVK / JAU; halt sprinkler irrigation; apply Tebuconazole or Chlorothalonil |
| **Cotton** (*Gossypium hirsutum*) | **Alternaria Leaf Spot** (*Alternaria macrospora*), **Cercospora Leaf Blight**, **Grey Mildew** (*Ramularia areola*) | Relative Humidity $> 75\%$, intermittent rainfall, dense canopy | Halt overhead watering to avoid droplet splash conidia dispersal; apply Propiconazole or Copper Oxychloride |

---

## Formal Mathematical & Logical Foundations

### 1. Knowledge Base & Production Rules

Let universe of discourse be agricultural plots $x \in \mathcal{P}$. The atomic propositions are:
- $\text{VulnerableCrop}(x)$: The plot is cultivated with Cotton or Groundnut.
- $\text{LocationGujarat}(x)$: Plot is situated in the high-density cash crop belt of Gujarat.
- $\text{LeafSpots}(x)$: Foliar lesions or necrotic spots observed on leaves.
- $\text{HighHumidity}(x)$: Relative humidity $\ge 80\%$ or sustained leaf wetness duration $> 8\text{ hrs}$.
- $\text{HighRiskAgroZone}(x)$: Plot belongs to an intensive epiphytotic vulnerability zone.
- $\text{FungalRisk}(x)$: High probability of fungal spore germination and tissue invasion.
- $\text{UrgentExpertInspection}(x)$: Escalation flag for Krishi Vigyan Kendra (KVK) physical diagnostic.
- $\text{WithholdOverheadIrrigation}(x)$: Ban on overhead sprinkler systems to prevent splash propagation.

The formal rule axioms in the Knowledge Base ($KB$) are:
$$\begin{aligned}
\mathbf{R_1} &: (\text{VulnerableCrop}(x) \land \text{LocationGujarat}(x)) \implies \text{HighRiskAgroZone}(x) \\
\mathbf{R_2} &: (\text{LeafSpots}(x) \land \text{HighHumidity}(x)) \implies \text{FungalRisk}(x) \\
\mathbf{R_3} &: (\text{FungalRisk}(x) \land \text{HighRiskAgroZone}(x)) \implies \text{UrgentExpertInspection}(x) \\
\mathbf{R_4} &: \text{FungalRisk}(x) \implies \text{WithholdOverheadIrrigation}(x) \\
\mathbf{R_5} &: (\text{FungalRisk}(x) \land \text{UrgentExpertInspection}(x)) \implies \text{ProphylacticFungicideAdvised}(x)
\end{aligned}$$

---

### 2. Auditable Modus Ponens Inference

The system applies classical **Modus Ponens** (Rule of Detachment):
$$\frac{\alpha, \quad \alpha \implies \beta}{\beta}$$

For ground plot $p_1$:
1. $\text{LeafSpots}(p_1) = \text{True}$ *(Farmer Observation)*
2. $\text{HighHumidity}(p_1) = \text{True}$ *(Agro-Meteorological Telemetry)*
3. From (1) and (2): $\text{LeafSpots}(p_1) \land \text{HighHumidity}(p_1)$
4. By Rule $\mathbf{R_2}$: $(\text{LeafSpots}(p_1) \land \text{HighHumidity}(p_1)) \implies \text{FungalRisk}(p_1)$
5. **Modus Ponens Deduction**: $\text{FungalRisk}(p_1) \vdash \mathbf{True}$
6. Concurrently, from $\mathbf{R_1}$: $\text{VulnerableCrop}(p_1) \land \text{LocationGujarat}(p_1) \implies \text{HighRiskAgroZone}(p_1)$
7. By Rule $\mathbf{R_3}$: $(\text{FungalRisk}(p_1) \land \text{HighRiskAgroZone}(p_1)) \implies \text{UrgentExpertInspection}(p_1)$
8. **Modus Ponens Deduction**: $\text{UrgentExpertInspection}(p_1) \vdash \mathbf{True}$

Every single deduction records:
- Antecedents satisfied & their origin timestamps
- Applied rule ID & agronomic rationale
- Deduced fact added to the active belief state

---

### 3. SymPy CNF Resolution Refutation Proof

In automated theorem proving, to prove $KB \models \mathcal{Q}$, the system applies **Proof by Refutation (Reductio ad Absurdum)**:
$$KB \models \mathcal{Q} \iff KB \land \neg \mathcal{Q} \text{ is UNSATISFIABLE}$$

#### Step A: CNF Transformation
Using SymPy's `to_cnf`, each implication $(\bigwedge A_i) \implies C$ is transformed via material implication $\neg (\bigwedge A_i) \lor C \equiv \bigvee \neg A_i \lor C$:
- $\text{CNF}(R_1) = \{\neg \text{VulnerableCrop} \lor \neg \text{LocationGujarat} \lor \text{HighRiskAgroZone}\}$
- $\text{CNF}(R_2) = \{\neg \text{LeafSpots} \lor \neg \text{HighHumidity} \lor \text{FungalRisk}\}$
- $\text{CNF}(R_3) = \{\neg \text{FungalRisk} \lor \neg \text{HighRiskAgroZone} \lor \text{UrgentExpertInspection}\}$
- Ground Facts: $\{\text{LeafSpots}\}, \{\text{HighHumidity}\}, \{\text{VulnerableCrop}\}, \{\text{LocationGujarat}\}$
- Negated Query $\neg \mathcal{Q}$: $\{\neg \text{UrgentExpertInspection}\}$ (or $\{\neg \text{FungalRisk}\}$)

#### Step B: Propositional Resolution Algorithm
For two clauses containing complementary literals $L$ and $\neg L$:
$$\frac{C_1 \lor L, \quad C_2 \lor \neg L}{C_1 \lor C_2}$$
The theorem prover repeatedly resolves pairs of clauses until the **Empty Clause ($\square$ / Contradiction)** is derived, demonstrating that the negated hypothesis is logically impossible.

#### Step C: SAT Verification
The engine queries SymPy's Davis-Putnam-Loveland-Logemann (DPLL) SAT solver:
$$\text{satisfiable}(KB \land \neg \mathcal{Q}) = \mathbf{False}$$
confirming unsatisfiability.

---

## System Architecture

```
Smart-Crop-Irrigation-AI-System/
├── advisory/
│   ├── __init__.py            # Package initialization
│   ├── models.py              # Data structures (Fact, Rule, DeductionStep, ResolutionStep)
│   ├── knowledge_base.py      # Rules R1-R5, Gujarat agro-pathology profiles (Cotton & Groundnut)
│   ├── modus_ponens.py        # Auditable forward-chaining deduction engine
│   ├── cnf_refutation.py      # SymPy CNF conversion & Resolution Refutation theorem prover
│   ├── engine.py              # High-level pipeline orchestrator
│   └── report_generator.py    # Terminal ASCII tables & Markdown audit export
├── examples/
│   ├── gujarat_groundnut_demo.py  # Standalone Saurashtra Groundnut Tikka advisory
│   ├── gujarat_cotton_demo.py     # Standalone Gujarat Bt-Cotton Alternaria advisory
│   └── counterfactual_analysis.py # Demonstrates false-positive prevention under low humidity
├── tests/
│   ├── __init__.py
│   └── test_advisory.py       # 8 unit & integration test cases
├── main.py                    # Complete CLI runner for Gujarat farmers
├── requirements.txt           # Python dependencies (sympy, tabulate, colorama, pytest)
└── README.md                  # Comprehensive architectural and mathematical documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13

### Install Dependencies
```bash
pip install -r requirements.txt
```

*(Core dependencies: `sympy>=1.12`, `tabulate>=0.9.0`, `colorama>=0.4.6`, `pytest>=7.4.0`)*

---

## Execution & Audit Examples

### Running the Main Advisory Case Studies
Execute the full advisory pipeline for both Gujarat Cotton and Groundnut:
```bash
python main.py
```

This generates terminal audit reports and exports:
- `audit_report_groundnut.md`
- `audit_report_cotton.md`

### Modus Ponens Audit Trail Sample
```text
========================================================================================
  [2] AUDITABLE MODUS PONENS DEDUCTION CHAIN
========================================================================================
Formal Rule of Inference Applied:  P ,  P -> Q  |-  Q

--- [STEP 2] Rule Fired: [R2] Fungal Disease Epiphytotic Risk Rule ---
  Antecedents Satisfied : LeafSpots(Plot-GJ-GND-101), HighHumidity(Plot-GJ-GND-101)
  Deduced Consequent    : FungalRisk(Plot-GJ-GND-101)
  Formal Schema         :
    Premise(s): LeafSpots(Plot-GJ-GND-101) ^ HighHumidity(Plot-GJ-GND-101)
    Rule [R2]: (LeafSpots(Plot-GJ-GND-101) ^ HighHumidity(Plot-GJ-GND-101)) -> FungalRisk(Plot-GJ-GND-101)
    Deduction:   [Modus Ponens] |- FungalRisk(Plot-GJ-GND-101)
  Agronomic Rationale   : Conidial germination of foliar fungi (Cercospora / Alternaria) requires free leaf moisture and relative humidity exceeding 80%.
  Audit Timestamp       : 2026-11-23 20:56:41

--- [STEP 3] Rule Fired: [R3] Urgent Agricultural Extension Escalation Rule ---
  Antecedents Satisfied : FungalRisk(Plot-GJ-GND-101), HighRiskAgroZone(Plot-GJ-GND-101)
  Deduced Consequent    : UrgentExpertInspection(Plot-GJ-GND-101)
  Formal Schema         :
    Premise(s): FungalRisk(Plot-GJ-GND-101) ^ HighRiskAgroZone(Plot-GJ-GND-101)
    Rule [R3]: (FungalRisk(Plot-GJ-GND-101) ^ HighRiskAgroZone(Plot-GJ-GND-101)) -> UrgentExpertInspection(Plot-GJ-GND-101)
    Deduction:   [Modus Ponens] |- UrgentExpertInspection(Plot-GJ-GND-101)
  Agronomic Rationale   : Rapid secondary spread in Gujarat cash crops demands immediate Krishi Vigyan Kendra (KVK) field inspection within 24-48 hours.
```

### Resolution Refutation Proof Sample
```text
--- THEOREM PROVING FOR: UrgentExpertInspection(Plot-GJ-GND-101) ---
  Proof Verdict            : PROVED (VALID THEOREM)
  SymPy SAT Status         : Verified Unsatisfiable (Theorem Proved via SymPy SAT)
  Proof Computation Time   : 0.81 ms
  Negated Query Clause     : C11 : ~UrgentExpertInspection(Plot-GJ-GND-101) [Negated Goal]

  Step-by-Step Resolution Refutation Steps:
+-----+------------------+------------------------------+----------------+--------------------+-------------------+
|   # | Parent Clauses   | Resolved On                  | Resolvent ID   | Resolvent Clause   | Status            |
+=====+==================+==============================+================+====================+===================+
|   1 | C1 + C8          | VulnerableCrop               | C12            | ...                | Valid Resolvent   |
|   2 | C2 + C10         | LeafSpots                    | C13            | ...                | Valid Resolvent   |
|   3 | C3 + C11         | UrgentExpertInspection       | C14            | ...                | Valid Resolvent   |
|   4 | C13 + C9         | HighHumidity                 | C15            | FungalRisk         | Valid Resolvent   |
|   5 | C12 + C7         | LocationGujarat              | C16            | HighRiskAgroZone   | Valid Resolvent   |
|   6 | C14 + C15        | FungalRisk                   | C17            | ~HighRiskAgroZone  | Valid Resolvent   |
|   7 | C16 + C17        | HighRiskAgroZone             | C18            | [] (Empty Clause)  | CONTRADICTION []  |
+-----+------------------+------------------------------+----------------+--------------------+-------------------+

  >> Q.E.D. Empty clause [] derived at resolution step. Hypothesis ~UrgentExpertInspection is REFUTED.
  >> Conclusion: UrgentExpertInspection is a sound logical consequence of the Knowledge Base.
```

### Actionable Agronomic Advisory
```text
+===========+==================================+===============================================================================================================================================+
| Urgency   | Category                         | Recommended Intervention                                                                                                                      |
+===========+==================================+===============================================================================================================================================+
| CRITICAL  | Field Escalation                 | Urgent physical inspection required. Contact ICAR-Directorate of Groundnut Research (DGR), Junagadh / KVK Amreli immediately.                 |
+-----------+----------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| HIGH      | Canopy & Irrigation Management   | IMMEDIATELY WITHHOLD OVERHEAD SPRINKLER IRRIGATION. Switch to drip or pause surface wetting until morning humidity drops.                     |
+-----------+----------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| HIGH      | Prophylactic Chemical Protection | Prepare preventative spray: Tebuconazole 25.9 EC @ 1.5 ml/L or Chlorothalonil 75 WP @ 2.0 g/L or Carbendazim 12% + Mancozeb 63% WP @ 2.0 g/L. |
+-----------+----------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
```

---

## Test Suite & Verification

The system includes a dedicated unit and integration test suite verifying mathematical soundness, edge cases, and counterfactuals:
```bash
pytest Smart-Crop-Irrigation-AI-System/tests -v
```

### Test Coverage Highlights:
- `test_rule_r2_modus_ponens_deduction`: Validates antecedent unification and deduction of `FungalRisk`.
- `test_rule_r3_urgent_inspection_flag`: Confirms automatic escalation to `UrgentExpertInspection`.
- `test_sympy_cnf_refutation_fungal_risk`: Proves formal derivation of $\square$ (Contradiction).
- `test_sympy_cnf_refutation_urgent_inspection`: Verifies resolution steps for escalation theorem.
- `test_counterfactual_missing_humidity_no_false_positive`: Guarantees that when humidity is normal, no false alarm is triggered.
- `test_cotton_gujarat_full_pipeline`: End-to-end audit for Saurashtra & Central Gujarat cotton plots.
- `test_groundnut_gujarat_full_pipeline`: End-to-end audit for Groundnut Tikka disease management.
- `test_audit_report_generation_text`: Validates text formatting, table layout, and Q.E.D. markers.

---

## Agronomic References

1. **ICAR - Directorate of Groundnut Research (DGR)**, Junagadh, Gujarat: *Compendium of Groundnut Diseases & Integrated Management of Tikka (Cercospora Leaf Spots)*.
2. **ICAR - Central Institute for Cotton Research (CICR)**: *Foliar Fungal Diseases of Cotton and Epiphytotic Forecast Models*.
3. **Junagadh Agricultural University (JAU) & Anand Agricultural University (AAU)**: *Gujarat Package of Practices for Kharif/Rabi Crops*.
4. **Russell, S., & Norvig, P.**: *Artificial Intelligence: A Modern Approach (4th ed.)* — Chapter 7 (Logical Agents) & Chapter 9 (Inference in First-Order Logic).
