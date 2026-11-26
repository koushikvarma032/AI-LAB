"""
Smart Irrigation MDP Model for Gujarat Agriculture
Specialized for Cotton Crop at Flowering Stage under Semi-Arid Gujarat Conditions.

State Space:
- 5 Soil Moisture Levels:
    0: Very Dry (<20%)
    1: Dry (20%-35%)
    2: Optimal (35%-60%)
    3: Wet (60%-80%)
    4: Waterlogged (>80%)
- 2 Rain Forecasts:
    0: No Rain Expected
    1: Rain Expected
Total: 10 Discrete States (State index = Moisture * 2 + RainForecast)

Action Space:
- 4 Irrigation Levels:
    0: None (0L)
    1: Low Irrigation (10L)
    2: Medium Irrigation (25L)
    3: High Irrigation (40L)
"""

from typing import Dict, List, Tuple
import numpy as np


class SmartIrrigationMDP:
    MOISTURE_LEVELS = [
        "Very Dry (<20%)",
        "Dry (20-35%)",
        "Optimal (35-60%)",
        "Wet (60-80%)",
        "Waterlogged (>80%)",
    ]

    RAIN_FORECASTS = [
        "No Rain Expected",
        "Rain Expected",
    ]

    ACTIONS = [0, 10, 25, 40]
    ACTION_NAMES = [
        "No Irrigation (0L)",
        "Low Irrigation (10L)",
        "Medium Irrigation (25L)",
        "High Irrigation (40L)",
    ]

    def __init__(
        self,
        temperature: float = 35.0,
        water_availability: str = "Medium",
        crop: str = "Cotton at Flowering",
        gamma: float = 0.90,
        epsilon: float = 1e-5,
    ):
        """
        Initializes the 10-State Markov Decision Process.

        Args:
            temperature: Ambient temperature in Celsius (e.g., 35 C in Gujarat).
            water_availability: 'Low', 'Medium', or 'High' water resource scarcity.
            crop: Crop and phenological growth stage.
            gamma: MDP discount factor.
            epsilon: Convergence threshold for Value Iteration.
        """
        self.temperature = temperature
        self.water_availability = water_availability
        self.crop = crop
        self.gamma = gamma
        self.epsilon = epsilon

        self.num_moisture = len(self.MOISTURE_LEVELS)  # 5
        self.num_rain = len(self.RAIN_FORECASTS)        # 2
        self.num_states = self.num_moisture * self.num_rain  # 10
        self.num_actions = len(self.ACTIONS)            # 4

        # Water conservation cost penalties based on resource availability
        self.water_cost = self._compute_water_costs()

        # Crop-specific stage rewards
        self.moisture_reward = self._compute_crop_rewards()

        # Transition matrix P[s, a, s'] and Reward matrix R[s, a, s']
        self.P = np.zeros((self.num_states, self.num_actions, self.num_states))
        self.R = np.zeros((self.num_states, self.num_actions, self.num_states))

        self._build_transition_and_reward_matrices()

    def _compute_water_costs(self) -> Dict[int, float]:
        """Calculates pumping and resource depletion penalty per liter."""
        multiplier = {"Low": 1.5, "Medium": 1.0, "High": 0.5}.get(self.water_availability, 1.0)
        base_costs = {0: 0.0, 10: -1.2, 25: -3.8, 40: -7.5}
        return {vol: cost * multiplier for vol, cost in base_costs.items()}

    def _compute_crop_rewards(self) -> Dict[int, float]:
        """
        Yield reward function for Cotton at Flowering.
        In Gujarat's Vertisols (black cotton soil), cotton is extremely vulnerable:
        - Severe drought (<20%) causes flower and boll abortion (-22.0)
        - Optimal moisture (35-60%) yields peak boll retention (+25.0)
        - Waterlogging (>80%) creates root hypoxia and severe shedding (-26.0)
        """
        return {
            0: -22.0,  # Very Dry: severe drought stress, square drop
            1: -7.0,   # Dry: water deficit, stress
            2: +25.0,  # Optimal: peak boll retention and flowering
            3: +4.0,   # Wet: acceptable, slight aeration drop
            4: -26.0,  # Waterlogged: severe penalty (root hypoxia, fungal rot, boll shedding)
        }

    def encode_state(self, moisture_idx: int, rain_idx: int) -> int:
        """Maps (moisture_level, rain_forecast) to state index 0..9."""
        return moisture_idx * self.num_rain + rain_idx

    def decode_state(self, state_idx: int) -> Tuple[int, int]:
        """Maps state index 0..9 to (moisture_level, rain_forecast)."""
        moisture_idx = state_idx // self.num_rain
        rain_idx = state_idx % self.num_rain
        return moisture_idx, rain_idx

    def map_inputs_to_state(self, soil_moisture_pct: float, rain_forecast_str: str) -> int:
        """
        Maps continuous/categorical farmer inputs to discrete state index.

        Args:
            soil_moisture_pct: e.g. 25.0
            rain_forecast_str: 'Rain expected' or 'No rain expected'
        """
        if soil_moisture_pct < 20.0:
            m_idx = 0
        elif soil_moisture_pct < 35.0:
            m_idx = 1
        elif soil_moisture_pct <= 60.0:
            m_idx = 2
        elif soil_moisture_pct <= 80.0:
            m_idx = 3
        else:
            m_idx = 4

        is_rain = 1 if "rain" in rain_forecast_str.lower() and "no" not in rain_forecast_str.lower() else 0
        return self.encode_state(m_idx, is_rain)

    def _build_transition_and_reward_matrices(self):
        """Constructs transition probability P(s'|s,a) and expected rewards R(s,a,s')."""
        # Markov weather forecast transition: P(next_forecast | current_forecast)
        forecast_transitions = {
            0: {0: 0.75, 1: 0.25},
            1: {0: 0.45, 1: 0.55},
        }

        # Temperature effect on evapotranspiration (ET):
        # At 35 C in Gujarat, ET loss is elevated without precipitation
        et_loss_prob = min(0.85, 0.50 + (self.temperature - 25.0) * 0.015) if self.temperature > 25 else 0.40

        for m in range(self.num_moisture):
            for r in range(self.num_rain):
                s = self.encode_state(m, r)

                # Weather realization given forecast r
                if r == 1:  # Rain Expected
                    weather_events = [
                        ("rain_light", 0.65 * 0.40, 0, 0),    # light shower (evaporates/minimal deep root gain)
                        ("rain_mod",   0.65 * 0.45, +1, 0),   # moderate shower (+1 level)
                        ("rain_heavy", 0.65 * 0.15, +2, 0),   # heavy monsoon downpour (+2 levels)
                        ("no_rain_et", 0.35 * et_loss_prob, 0, -1),  # rain delayed/missed, high ET drop
                        ("no_rain_0",  0.35 * (1.0 - et_loss_prob), 0, 0),
                    ]
                else:  # No Rain Expected
                    weather_events = [
                        ("rain_surprise", 0.15, +1, 0),       # unforecasted shower
                        ("no_rain_et",    0.85 * et_loss_prob, 0, -1),
                        ("no_rain_0",     0.85 * (1.0 - et_loss_prob), 0, 0),
                    ]

                for a_idx, a_val in enumerate(self.ACTIONS):
                    # Irrigation boost distribution:
                    if a_val == 0:
                        irr_events = [(0, 1.0)]
                    elif a_val == 10:
                        irr_events = [(1, 0.85), (0, 0.15)]
                    elif a_val == 25:
                        irr_events = [(2, 0.85), (1, 0.15)]
                    elif a_val == 40:
                        irr_events = [(3, 0.85), (2, 0.15)]

                    for _, p_w, rain_delta, et_delta in weather_events:
                        for irr_delta, p_irr in irr_events:
                            p_joint = p_w * p_irr

                            next_m = m + irr_delta + rain_delta + et_delta
                            next_m = max(0, min(self.num_moisture - 1, next_m))

                            for next_r, p_rf in forecast_transitions[r].items():
                                next_s = self.encode_state(next_m, next_r)
                                prob = p_joint * p_rf
                                self.P[s, a_idx, next_s] += prob

                                reward = self.moisture_reward[next_m] + self.water_cost[a_val]
                                self.R[s, a_idx, next_s] = reward

        # Enforce exact stochastic normalization
        for s in range(self.num_states):
            for a in range(self.num_actions):
                row_sum = np.sum(self.P[s, a, :])
                if row_sum > 0:
                    self.P[s, a, :] /= row_sum

    def solve_value_iteration(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, int]:
        """
        Solves the MDP using Value Iteration via the Bellman Optimality Equation:
        V_{k+1}(s) = max_a sum_{s'} P(s'|s,a) [ R(s,a,s') + gamma * V_k(s') ]

        Returns:
            optimal_v: Optimal state values (length 10)
            optimal_policy: Index of optimal action per state (length 10)
            q_table: Action-value table Q(s, a) (shape 10 x 4)
            iterations: Number of iterations taken to converge
        """
        V = np.zeros(self.num_states)
        iterations = 0

        while True:
            delta = 0.0
            V_new = np.zeros(self.num_states)

            for s in range(self.num_states):
                q_vals = [
                    sum(
                        self.P[s, a, s_next] * (self.R[s, a, s_next] + self.gamma * V[s_next])
                        for s_next in range(self.num_states)
                    )
                    for a in range(self.num_actions)
                ]
                V_new[s] = max(q_vals)
                delta = max(delta, abs(V_new[s] - V[s]))

            V = V_new
            iterations += 1
            if delta < self.epsilon or iterations >= 2000:
                break

        # Compute Q-values and extract policy
        q_table = np.zeros((self.num_states, self.num_actions))
        optimal_policy = np.zeros(self.num_states, dtype=int)

        for s in range(self.num_states):
            for a in range(self.num_actions):
                q_table[s, a] = sum(
                    self.P[s, a, s_next] * (self.R[s, a, s_next] + self.gamma * V[s_next])
                    for s_next in range(self.num_states)
                )
            optimal_policy[s] = int(np.argmax(q_table[s]))

        return V, optimal_policy, q_table, iterations
