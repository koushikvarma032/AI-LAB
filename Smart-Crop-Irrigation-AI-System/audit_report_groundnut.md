# Smart Crop Disease Advisory Report

- **Farmer:** Rameshbhai Patel
- **Region:** Saurashtra (Rajkot / Junagadh), Gujarat
- **Crop:** Groundnut (Arachis hypogaea / GG-20)
- **Plot:** Plot-GJ-GND-101
- **Generated At:** 2026-11-23 21:00:14

## 1. Observed Evidence

| # | Fact (FOL) | Source | Timestamp |
|---|---|---|---|
| 1 | `VulnerableCrop(Plot-GJ-GND-101)` | Crop Registry | 2026-11-23 21:00:14 |
| 2 | `LocationGujarat(Plot-GJ-GND-101)` | Geographic Telemetry | 2026-11-23 21:00:14 |
| 3 | `LeafSpots(Plot-GJ-GND-101)` | Farmer Field Observation | 2026-11-23 21:00:14 |
| 4 | `HighHumidity(Plot-GJ-GND-101)` | Agro-Weather Station (RH > 80%) | 2026-11-23 21:00:14 |
| 5 | `SoilMoistureHigh(Plot-GJ-GND-101)` | Soil Tensiometer Sensor | 2026-11-23 21:00:14 |

## 2. Auditable Modus Ponens Deduction Chain

### Step 1: Rule `R1` - Vulnerable Agro-Climatic Host Rule

- **Antecedents:** `VulnerableCrop(Plot-GJ-GND-101), LocationGujarat(Plot-GJ-GND-101)`
- **Consequent:** `HighRiskAgroZone(Plot-GJ-GND-101)`
```text
Premise(s): VulnerableCrop(Plot-GJ-GND-101) ^ LocationGujarat(Plot-GJ-GND-101)
Rule [R1]: (VulnerableCrop(Plot-GJ-GND-101) ^ LocationGujarat(Plot-GJ-GND-101)) -> HighRiskAgroZone(Plot-GJ-GND-101)
Deduction:   [Modus Ponens] |- HighRiskAgroZone(Plot-GJ-GND-101)
```
- **Rationale:** Intensive cultivation in Saurashtra and Central Gujarat creates microclimates where spore inoculum builds rapidly.

### Step 2: Rule `R2` - Fungal Disease Epiphytotic Risk Rule

- **Antecedents:** `LeafSpots(Plot-GJ-GND-101), HighHumidity(Plot-GJ-GND-101)`
- **Consequent:** `FungalRisk(Plot-GJ-GND-101)`
```text
Premise(s): LeafSpots(Plot-GJ-GND-101) ^ HighHumidity(Plot-GJ-GND-101)
Rule [R2]: (LeafSpots(Plot-GJ-GND-101) ^ HighHumidity(Plot-GJ-GND-101)) -> FungalRisk(Plot-GJ-GND-101)
Deduction:   [Modus Ponens] |- FungalRisk(Plot-GJ-GND-101)
```
- **Rationale:** Conidial germination of foliar fungi (Cercospora / Alternaria) requires free leaf moisture and relative humidity exceeding 80%.

### Step 3: Rule `R3` - Urgent Agricultural Extension Escalation Rule

- **Antecedents:** `FungalRisk(Plot-GJ-GND-101), HighRiskAgroZone(Plot-GJ-GND-101)`
- **Consequent:** `UrgentExpertInspection(Plot-GJ-GND-101)`
```text
Premise(s): FungalRisk(Plot-GJ-GND-101) ^ HighRiskAgroZone(Plot-GJ-GND-101)
Rule [R3]: (FungalRisk(Plot-GJ-GND-101) ^ HighRiskAgroZone(Plot-GJ-GND-101)) -> UrgentExpertInspection(Plot-GJ-GND-101)
Deduction:   [Modus Ponens] |- UrgentExpertInspection(Plot-GJ-GND-101)
```
- **Rationale:** Rapid secondary spread in Gujarat cash crops demands immediate Krishi Vigyan Kendra (KVK) field inspection within 24-48 hours.

### Step 4: Rule `R4` - Canopy Moisture Control & Irrigation Advisory Rule

- **Antecedents:** `FungalRisk(Plot-GJ-GND-101)`
- **Consequent:** `WithholdOverheadIrrigation(Plot-GJ-GND-101)`
```text
Premise(s): FungalRisk(Plot-GJ-GND-101)
Rule [R4]: (FungalRisk(Plot-GJ-GND-101)) -> WithholdOverheadIrrigation(Plot-GJ-GND-101)
Deduction:   [Modus Ponens] |- WithholdOverheadIrrigation(Plot-GJ-GND-101)
```
- **Rationale:** Overhead sprinkler irrigation prolongs leaf wetness duration (LWD) and propels fungal conidia across canopy rows.

### Step 5: Rule `R5` - Prophylactic Chemical/Bio-fungicide Barrier Rule

- **Antecedents:** `FungalRisk(Plot-GJ-GND-101), UrgentExpertInspection(Plot-GJ-GND-101)`
- **Consequent:** `ProphylacticFungicideAdvised(Plot-GJ-GND-101)`
```text
Premise(s): FungalRisk(Plot-GJ-GND-101) ^ UrgentExpertInspection(Plot-GJ-GND-101)
Rule [R5]: (FungalRisk(Plot-GJ-GND-101) ^ UrgentExpertInspection(Plot-GJ-GND-101)) -> ProphylacticFungicideAdvised(Plot-GJ-GND-101)
Deduction:   [Modus Ponens] |- ProphylacticFungicideAdvised(Plot-GJ-GND-101)
```
- **Rationale:** Initiate contact protective fungicide application (e.g. Mancozeb 75% WP @ 2g/L or Trichoderma viride) pending specialist diagnostic.

## 3. SymPy CNF Refutation Proofs

### Query: `FungalRisk(Plot-GJ-GND-101)`

- **Verdict:** **PROVED (VALID)**
- **SymPy SAT Solver:** Verified Unsatisfiable (Theorem Proved via SymPy SAT)
- **Computation Time:** 86.59 ms

#### Step-by-Step Resolution Refutation

| Step | Parents | Resolved Literal | Resolvent ID | Resolvent Clause | Status |
|---|---|---|---|---|---|
| 1 | C1 + C6 | `~VulnerableCrop_Plot_GJ_GND_101` | C12 | `HighRiskAgroZone_Plot_GJ_GND_101 v ~LocationGujarat_Plot_GJ_GND_101` | Resolvent |
| 2 | C7 + C12 | `LocationGujarat_Plot_GJ_GND_101` | C13 | `HighRiskAgroZone_Plot_GJ_GND_101` | Resolvent |
| 3 | C1 + C7 | `~LocationGujarat_Plot_GJ_GND_101` | C14 | `HighRiskAgroZone_Plot_GJ_GND_101 v ~VulnerableCrop_Plot_GJ_GND_101` | Resolvent |
| 4 | C2 + C8 | `~LeafSpots_Plot_GJ_GND_101` | C15 | `FungalRisk_Plot_GJ_GND_101 v ~HighHumidity_Plot_GJ_GND_101` | Resolvent |
| 5 | C9 + C15 | `HighHumidity_Plot_GJ_GND_101` | C16 | `FungalRisk_Plot_GJ_GND_101` | Resolvent |
| 6 | C11 + C16 | `~FungalRisk_Plot_GJ_GND_101` | C17 | `[] (Empty Clause / Contradiction)` | **Contradiction ($\square$)** |

### Query: `UrgentExpertInspection(Plot-GJ-GND-101)`

- **Verdict:** **PROVED (VALID)**
- **SymPy SAT Solver:** Verified Unsatisfiable (Theorem Proved via SymPy SAT)
- **Computation Time:** 6.12 ms

#### Step-by-Step Resolution Refutation

| Step | Parents | Resolved Literal | Resolvent ID | Resolvent Clause | Status |
|---|---|---|---|---|---|
| 1 | C1 + C6 | `~VulnerableCrop_Plot_GJ_GND_101` | C12 | `HighRiskAgroZone_Plot_GJ_GND_101 v ~LocationGujarat_Plot_GJ_GND_101` | Resolvent |
| 2 | C7 + C12 | `LocationGujarat_Plot_GJ_GND_101` | C13 | `HighRiskAgroZone_Plot_GJ_GND_101` | Resolvent |
| 3 | C1 + C7 | `~LocationGujarat_Plot_GJ_GND_101` | C14 | `HighRiskAgroZone_Plot_GJ_GND_101 v ~VulnerableCrop_Plot_GJ_GND_101` | Resolvent |
| 4 | C2 + C8 | `~LeafSpots_Plot_GJ_GND_101` | C15 | `FungalRisk_Plot_GJ_GND_101 v ~HighHumidity_Plot_GJ_GND_101` | Resolvent |
| 5 | C9 + C15 | `HighHumidity_Plot_GJ_GND_101` | C16 | `FungalRisk_Plot_GJ_GND_101` | Resolvent |
| 6 | C4 + C16 | `~FungalRisk_Plot_GJ_GND_101` | C17 | `WithholdOverheadIrrigation_Plot_GJ_GND_101` | Resolvent |
| 7 | C2 + C9 | `~HighHumidity_Plot_GJ_GND_101` | C18 | `FungalRisk_Plot_GJ_GND_101 v ~LeafSpots_Plot_GJ_GND_101` | Resolvent |
| 8 | C3 + C11 | `UrgentExpertInspection_Plot_GJ_GND_101` | C19 | `~FungalRisk_Plot_GJ_GND_101 v ~HighRiskAgroZone_Plot_GJ_GND_101` | Resolvent |
| 9 | C13 + C19 | `HighRiskAgroZone_Plot_GJ_GND_101` | C20 | `~FungalRisk_Plot_GJ_GND_101` | Resolvent |
| 10 | C16 + C20 | `FungalRisk_Plot_GJ_GND_101` | C21 | `[] (Empty Clause / Contradiction)` | **Contradiction ($\square$)** |

## 4. Agronomic Advisories

| Urgency | Category | Action | Basis |
|---|---|---|---|
| **CRITICAL** | Field Escalation | Urgent physical inspection required. Contact ICAR-Directorate of Groundnut Research (DGR), Junagadh / KVK Amreli immediately. | Foliar fungal pathogens in high-humidity Gujarat zones can multiply exponentially within 48-72 hours, resulting in 30-50% defoliation. |
| **HIGH** | Canopy & Irrigation Management | IMMEDIATELY WITHHOLD OVERHEAD SPRINKLER IRRIGATION. Switch to drip or pause surface wetting until morning humidity drops. | Overhead water droplets physically dislodge conidia (spores) and increase Leaf Wetness Duration (LWD), accelerating disease germination. |
| **HIGH** | Prophylactic Chemical Protection | Prepare preventative spray: Tebuconazole 25.9 EC @ 1.5 ml/L or Chlorothalonil 75 WP @ 2.0 g/L or Carbendazim 12% + Mancozeb 63% WP @ 2.0 g/L. | High risk of primary/secondary infection by Early Leaf Spot / Tikka (Cercospora arachidicola), Late Leaf Spot / Tikka (Phaeoisariopsis personata / Cercosporidium personatum), Rust (Puccinia arachidis). Protective spray creates a fungistatic chemical barrier on leaf cuticles. |
| **MEDIUM** | Cultural Sanitation | Collect and destroy severely spotted lower senescent leaves; maintain inter-row ventilation. | Eliminates the primary inoculum reservoir residing in microclimates close to moist Gujarat black-cotton (vertisol) soils. |
