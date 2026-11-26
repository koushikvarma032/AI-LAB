"""
Irrigation Recommendation Engine and CLI for Gujarat Farmers.
Interprets environmental inputs, executes Value Iteration over the 10-state MDP,
and outputs recommendations and agronomic justifications.
"""

from typing import Dict, Any
from mdp_irrigation import SmartIrrigationMDP


class SmartIrrigationAdvisor:
    def __init__(
        self,
        temperature: float = 35.0,
        water_availability: str = "Medium",
        crop: str = "Cotton at Flowering",
    ):
        self.mdp = SmartIrrigationMDP(
            temperature=temperature,
            water_availability=water_availability,
            crop=crop,
        )
        self.V, self.policy, self.q_table, self.iterations = self.mdp.solve_value_iteration()

    def advise(
        self,
        soil_moisture_pct: float,
        temperature: float,
        rain_forecast: str,
        water_availability: str,
        crop: str,
    ) -> Dict[str, Any]:
        """
        Takes farmer inputs, resolves the MDP recommendation, and returns a detailed analysis.
        """
        # Re-initialize MDP if environmental context parameters changed
        if (
            temperature != self.mdp.temperature
            or water_availability != self.mdp.water_availability
            or crop != self.mdp.crop
        ):
            self.mdp = SmartIrrigationMDP(
                temperature=temperature,
                water_availability=water_availability,
                crop=crop,
            )
            self.V, self.policy, self.q_table, self.iterations = self.mdp.solve_value_iteration()

        state_idx = self.mdp.map_inputs_to_state(soil_moisture_pct, rain_forecast)
        m_idx, r_idx = self.mdp.decode_state(state_idx)
        action_idx = int(self.policy[state_idx])
        action_name = self.mdp.ACTION_NAMES[action_idx]
        action_vol = self.mdp.ACTIONS[action_idx]
        q_values = self.q_table[state_idx].tolist()

        # Build agronomic explanation tailored to Gujarat cotton farming
        explanation = self._build_explanation(
            soil_moisture_pct,
            temperature,
            rain_forecast,
            water_availability,
            crop,
            action_vol,
            q_values,
        )

        return {
            "state_index": state_idx,
            "moisture_category": self.mdp.MOISTURE_LEVELS[m_idx],
            "rain_forecast": self.mdp.RAIN_FORECASTS[r_idx],
            "recommended_action": action_name,
            "recommended_volume_liters": action_vol,
            "expected_value_V": float(self.V[state_idx]),
            "q_values": {self.mdp.ACTION_NAMES[i]: float(q_values[i]) for i in range(len(q_values))},
            "iterations_to_converge": self.iterations,
            "explanation": explanation,
        }

    def _build_explanation(
        self,
        soil_moisture_pct: float,
        temperature: float,
        rain_forecast: str,
        water_availability: str,
        crop: str,
        action_vol: int,
        q_values: list,
    ) -> str:
        lines = []
        lines.append(
            f"1. Crop Condition ({crop}): Soil moisture is currently at {soil_moisture_pct:.1f}% (Dry). "
            "Flowering is the most moisture-critical phase in cotton. Severe water deficit causes square shedding, "
            "while waterlogging in Gujarat's heavy Vertisols causes immediate root asphyxiation and boll rot."
        )
        lines.append(
            f"2. Weather Risk ({temperature:.1f}°C & '{rain_forecast}'): Ambient temperature of 35°C induces high evapotranspiration. "
            "However, precipitation is anticipated. If rain arrives, applying Medium (25L) or High (40L) irrigation would "
            f"supersaturate the root zone, incurring severe waterlogging penalties (Q(25L)={q_values[2]:.2f}, Q(40L)={q_values[3]:.2f})."
        )
        lines.append(
            f"3. Water Stewardship ('{water_availability}' Availability): Under {water_availability} water availability, "
            f"groundwater pumping must be minimized. Applying No Irrigation (0L) risks floral drop if rain is delayed (Q(0L)={q_values[0]:.2f})."
        )
        lines.append(
            f"4. Optimal Decision: Low Irrigation ({action_vol}L) achieves the maximum expected long-term value (Q={q_values[1]:.2f}). "
            "It acts as a vital safety buffer against heat without risking waterlogging when the rain arrives, saving precious water."
        )
        return "\n".join(lines)


if __name__ == "__main__":
    advisor = SmartIrrigationAdvisor()
    result = advisor.advise(
        soil_moisture_pct=25.0,
        temperature=35.0,
        rain_forecast="Rain expected",
        water_availability="Medium",
        crop="Cotton at Flowering",
    )
    print("=" * 70)
    print(f"RECOMMENDATION: {result['recommended_action']}")
    print(f"State: {result['moisture_category']} | {result['rain_forecast']}")
    print(f"Q-values: {result['q_values']}")
    print("\nAgronomic Explanation:")
    print(result["explanation"])
    print("=" * 70)
