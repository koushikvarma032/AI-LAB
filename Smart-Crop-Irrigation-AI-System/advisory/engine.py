"""
Orchestration engine integrating Knowledge Base, Modus Ponens forward deduction,
SymPy CNF refutation theorem proving, and actionable agronomic advisory generation.
"""

from typing import List, Dict, Optional, Tuple, Any
from .models import (
    Fact,
    Rule,
    DeductionStep,
    RefutationProofResult,
    AgronomicAdvisoryItem,
    AdvisoryReport
)
from .knowledge_base import AgriculturalKnowledgeBase, get_gujarat_crop_profile
from .modus_ponens import ModusPonensDeductionEngine
from .cnf_refutation import SymPyCNFRefutationEngine


class SmartCropAdvisoryEngine:
    """
    Unified AI engine combining:
    1. Auditable Modus Ponens Forward Chaining
    2. Formal SymPy CNF Resolution Refutation Proofs
    3. Crop-specific Agronomic Disease Diagnostics for Gujarat
    """
    def __init__(self, use_extended_rules: bool = True):
        self.kb = AgriculturalKnowledgeBase(use_extended_rules=use_extended_rules)
        self.mp_engine = ModusPonensDeductionEngine(self.kb)
        self.cnf_engine = SymPyCNFRefutationEngine()

    def analyze_field(
        self,
        farmer_name: str,
        region: str,
        crop: str,
        plot_id: str,
        leaf_spots_observed: bool,
        high_humidity_observed: bool,
        soil_moisture_high: bool = True,
        extended_facts: Optional[List[Fact]] = None
    ) -> AdvisoryReport:
        """
        Executes full reasoning pipeline for a farmer in Gujarat.
        """
        # Step 1: Ground atomic facts
        facts: List[Fact] = []

        is_gujarat = "gujarat" in region.lower()
        is_cotton_or_groundnut = any(c in crop.lower() for c in ["cotton", "groundnut", "peanut", "kapas", "magfali"])

        if is_cotton_or_groundnut:
            facts.append(Fact("VulnerableCrop", plot_id, True, source="Crop Registry"))
        if is_gujarat:
            facts.append(Fact("LocationGujarat", plot_id, True, source="Geographic Telemetry"))
        if leaf_spots_observed:
            facts.append(Fact("LeafSpots", plot_id, True, source="Farmer Field Observation"))
        if high_humidity_observed:
            facts.append(Fact("HighHumidity", plot_id, True, source="Agro-Weather Station (RH > 80%)"))
        if soil_moisture_high:
            facts.append(Fact("SoilMoistureHigh", plot_id, True, source="Soil Tensiometer Sensor"))

        if extended_facts:
            facts.extend(extended_facts)

        # Step 2: Modus Ponens Deductive Chaining
        deduced_facts, deduction_chain = self.mp_engine.infer(facts, plot_id)
        deduced_predicates = {f.predicate for f in deduced_facts if f.value}

        # Step 3: SymPy CNF Resolution Refutation Proofs
        refutation_proofs: Dict[str, RefutationProofResult] = {}

        # Prove FungalRisk
        if "FungalRisk" in deduced_predicates:
            proof_fr = self.cnf_engine.prove(
                rules=self.kb.rules,
                facts=facts,
                query_predicate="FungalRisk",
                target=plot_id
            )
            refutation_proofs["FungalRisk"] = proof_fr

        # Prove UrgentExpertInspection
        if "UrgentExpertInspection" in deduced_predicates:
            proof_inspection = self.cnf_engine.prove(
                rules=self.kb.rules,
                facts=facts,
                query_predicate="UrgentExpertInspection",
                target=plot_id
            )
            refutation_proofs["UrgentExpertInspection"] = proof_inspection

        # Step 4: Synthesize Agronomic Advisory based on Crop Profile & Proofs
        advisories = self._generate_advisories(
            crop=crop,
            region=region,
            deduced_predicates=deduced_predicates,
            plot_id=plot_id
        )

        return AdvisoryReport(
            farmer_name=farmer_name,
            region=region,
            crop=crop,
            plot_id=plot_id,
            observed_facts=facts,
            deduction_chain=deduction_chain,
            refutation_proofs=refutation_proofs,
            advisories=advisories
        )

    def _generate_advisories(
        self,
        crop: str,
        region: str,
        deduced_predicates: set,
        plot_id: str
    ) -> List[AgronomicAdvisoryItem]:
        """
        Translates deduced logical risk conclusions into authoritative agronomic advisories.
        """
        items: List[AgronomicAdvisoryItem] = []
        crop_profile = get_gujarat_crop_profile(crop)

        if "UrgentExpertInspection" in deduced_predicates:
            items.append(AgronomicAdvisoryItem(
                category="Field Escalation",
                recommendation=f"Urgent physical inspection required. Contact {crop_profile.get('kvk_contact_gujarat', 'Local KVK')} immediately.",
                urgency="CRITICAL",
                scientific_basis="Foliar fungal pathogens in high-humidity Gujarat zones can multiply exponentially within 48-72 hours, resulting in 30-50% defoliation."
            ))

        if "WithholdOverheadIrrigation" in deduced_predicates:
            items.append(AgronomicAdvisoryItem(
                category="Canopy & Irrigation Management",
                recommendation="IMMEDIATELY WITHHOLD OVERHEAD SPRINKLER IRRIGATION. Switch to drip or pause surface wetting until morning humidity drops.",
                urgency="HIGH",
                scientific_basis="Overhead water droplets physically dislodge conidia (spores) and increase Leaf Wetness Duration (LWD), accelerating disease germination."
            ))

        if "FungalRisk" in deduced_predicates:
            pathogens = ", ".join(crop_profile.get("suspected_pathogens", ["Foliar fungi"])[:3])
            spray = crop_profile.get("recommended_fungicide_spray", "Protective contact fungicide")
            items.append(AgronomicAdvisoryItem(
                category="Prophylactic Chemical Protection",
                recommendation=f"Prepare preventative spray: {spray}.",
                urgency="HIGH",
                scientific_basis=f"High risk of primary/secondary infection by {pathogens}. Protective spray creates a fungistatic chemical barrier on leaf cuticles."
            ))

            items.append(AgronomicAdvisoryItem(
                category="Cultural Sanitation",
                recommendation="Collect and destroy severely spotted lower senescent leaves; maintain inter-row ventilation.",
                urgency="MEDIUM",
                scientific_basis="Eliminates the primary inoculum reservoir residing in microclimates close to moist Gujarat black-cotton (vertisol) soils."
            ))

        return items
