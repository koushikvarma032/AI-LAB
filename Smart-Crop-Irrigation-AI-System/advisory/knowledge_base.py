"""
Knowledge Base definition for Cotton & Groundnut crop disease reasoning in Gujarat.
Contains formal agronomic production rules and regional crop pathology profiles.
"""

from typing import List, Dict, Any
from .models import Rule


def get_default_rules() -> List[Rule]:
    """
    Returns the formal inference rules governing crop pathology.
    Notice R2 and R3 as explicitly required by the problem statement.
    """
    return [
        Rule(
            rule_id="R1",
            name="Vulnerable Agro-Climatic Host Rule",
            antecedents=["VulnerableCrop", "LocationGujarat"],
            consequent="HighRiskAgroZone",
            description="Cotton and groundnut monocultures in humid Gujarat agro-climatic zones are highly prone to foliar epiphytotics.",
            agronomic_rationale="Intensive cultivation in Saurashtra and Central Gujarat creates microclimates where spore inoculum builds rapidly.",
            source_reference="Junagadh Agricultural University (JAU) & AAU Plant Pathology Compendium"
        ),
        Rule(
            rule_id="R2",
            name="Fungal Disease Epiphytotic Risk Rule",
            antecedents=["LeafSpots", "HighHumidity"],
            consequent="FungalRisk",
            description="(LeafSpots(x) AND HighHumidity(x)) -> FungalRisk(x)",
            agronomic_rationale="Conidial germination of foliar fungi (Cercospora / Alternaria) requires free leaf moisture and relative humidity exceeding 80%.",
            source_reference="ICAR-Directorate of Groundnut Research (DGR), ICAR-Central Institute for Cotton Research (CICR)"
        ),
        Rule(
            rule_id="R3",
            name="Urgent Agricultural Extension Escalation Rule",
            antecedents=["FungalRisk", "HighRiskAgroZone"],
            consequent="UrgentExpertInspection",
            description="(FungalRisk(x) AND HighRiskAgroZone(x)) -> UrgentExpertInspection(x)",
            agronomic_rationale="Rapid secondary spread in Gujarat cash crops demands immediate Krishi Vigyan Kendra (KVK) field inspection within 24-48 hours.",
            source_reference="Gujarat State Department of Agriculture - Pest Surveillance and Advisory System (e-Pest)"
        ),
        Rule(
            rule_id="R4",
            name="Canopy Moisture Control & Irrigation Advisory Rule",
            antecedents=["FungalRisk"],
            consequent="WithholdOverheadIrrigation",
            description="FungalRisk(x) -> WithholdOverheadIrrigation(x)",
            agronomic_rationale="Overhead sprinkler irrigation prolongs leaf wetness duration (LWD) and propels fungal conidia across canopy rows.",
            source_reference="FAO Irrigation and Water Management Bulletin #56 / JAU Water Technology Centre"
        ),
        Rule(
            rule_id="R5",
            name="Prophylactic Chemical/Bio-fungicide Barrier Rule",
            antecedents=["FungalRisk", "UrgentExpertInspection"],
            consequent="ProphylacticFungicideAdvised",
            description="(FungalRisk(x) AND UrgentExpertInspection(x)) -> ProphylacticFungicideAdvised(x)",
            agronomic_rationale="Initiate contact protective fungicide application (e.g. Mancozeb 75% WP @ 2g/L or Trichoderma viride) pending specialist diagnostic.",
            source_reference="Central Insecticides Board & Registration Committee (CIBRC) Crop Protection Guidelines"
        )
    ]


def get_direct_rules() -> List[Rule]:
    """
    Returns the canonical direct rules for straightforward demonstration,
    featuring the explicit chain: R2: (LeafSpots AND HighHumidity) -> FungalRisk,
    and R3: FungalRisk -> UrgentExpertInspection.
    """
    return [
        Rule(
            rule_id="R2",
            name="Fungal Risk Rule",
            antecedents=["LeafSpots", "HighHumidity"],
            consequent="FungalRisk",
            description="(LeafSpots(x) AND HighHumidity(x)) -> FungalRisk(x)",
            agronomic_rationale="Leaf spots paired with ambient relative humidity > 80% create ideal incubation for fungal spore propagation.",
            source_reference="ICAR Technical Bulletin on Cotton & Groundnut Foliar Pathologies"
        ),
        Rule(
            rule_id="R3",
            name="Urgent Inspection Flag Rule",
            antecedents=["FungalRisk"],
            consequent="UrgentExpertInspection",
            description="FungalRisk(x) -> UrgentExpertInspection(x)",
            agronomic_rationale="Confirmed fungal risk warrants on-field diagnostic verification by agronomy experts to prevent harvest loss.",
            source_reference="KVK Gujarat Extension Alert Protocol"
        ),
        Rule(
            rule_id="R4",
            name="Irrigation Mitigation Rule",
            antecedents=["FungalRisk"],
            consequent="WithholdOverheadIrrigation",
            description="FungalRisk(x) -> WithholdOverheadIrrigation(x)",
            agronomic_rationale="Halt overhead sprinkler systems immediately to curb spore dissemination through splash droplets.",
            source_reference="Micro-Irrigation & Canopy Management Advisory"
        )
    ]


def get_gujarat_crop_profile(crop: str) -> Dict[str, Any]:
    """
    Returns agronomic context for Gujarat crops (Cotton / Groundnut).
    """
    crop_lower = crop.lower()
    if "cotton" in crop_lower:
        return {
            "crop": "Cotton (Gossypium hirsutum / herbaceum)",
            "major_gujarat_districts": ["Rajkot", "Surendranagar", "Amreli", "Bhavnagar", "Vadodara", "Bharuch"],
            "suspected_pathogens": [
                "Alternaria Leaf Spot (Alternaria macrospora)",
                "Cercospora Leaf Spot (Cercospora gossypina)",
                "Grey Mildew / Dahiya Disease (Ramularia areola)",
                "Bacterial Blight / Angular Leaf Spot (Xanthomonas citri pv. malvacearum)"
            ],
            "critical_weather_triggers": {
                "relative_humidity": "> 75%",
                "temperature": "24°C - 30°C",
                "leaf_wetness_hours": "> 8 hours continuous"
            },
            "recommended_fungicide_spray": "Mancozeb 75 WP @ 2.5 g/L or Propiconazole 25 EC @ 1 ml/L or Copper Oxychloride 50 WP @ 2.5 g/L",
            "kvk_contact_gujarat": "KVK Targhadia (Rajkot) / JAU Directorate of Extension Education"
        }
    elif "groundnut" in crop_lower or "peanut" in crop_lower:
        return {
            "crop": "Groundnut / Peanut (Arachis hypogaea)",
            "major_gujarat_districts": ["Junagadh", "Rajkot", "Amreli", "Gir Somnath", "Jamnagar", "Porbandar"],
            "suspected_pathogens": [
                "Early Leaf Spot / Tikka (Cercospora arachidicola)",
                "Late Leaf Spot / Tikka (Phaeoisariopsis personata / Cercosporidium personatum)",
                "Rust (Puccinia arachidis)",
                "Collar Rot (Aspergillus niger)"
            ],
            "critical_weather_triggers": {
                "relative_humidity": "> 80%",
                "temperature": "25°C - 32°C",
                "leaf_wetness_hours": "> 10 hours continuous"
            },
            "recommended_fungicide_spray": "Tebuconazole 25.9 EC @ 1.5 ml/L or Chlorothalonil 75 WP @ 2.0 g/L or Carbendazim 12% + Mancozeb 63% WP @ 2.0 g/L",
            "kvk_contact_gujarat": "ICAR-Directorate of Groundnut Research (DGR), Junagadh / KVK Amreli"
        }
    else:
        return {
            "crop": crop,
            "major_gujarat_districts": ["Gujarat Agricultural Zones"],
            "suspected_pathogens": ["Foliar fungal pathogens"],
            "critical_weather_triggers": {"relative_humidity": "> 80%"},
            "recommended_fungicide_spray": "Broad-spectrum protective contact fungicide",
            "kvk_contact_gujarat": "District Krishi Vigyan Kendra"
        }


class AgriculturalKnowledgeBase:
    """Encapsulates rules, facts, and profile retrieval for an inference session."""
    def __init__(self, use_extended_rules: bool = True):
        self.rules: List[Rule] = get_default_rules() if use_extended_rules else get_direct_rules()

    def get_rule_by_id(self, rule_id: str) -> Rule:
        for r in self.rules:
            if r.rule_id == rule_id:
                return r
        raise KeyError(f"Rule ID {rule_id} not found in Knowledge Base.")

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
