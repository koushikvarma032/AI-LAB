"""
Unit Tests for Smart Irrigation MDP System.
Verifies state encoding, transition matrix probabilities, value iteration convergence,
and optimal policy recommendations for Gujarat Cotton farming.
"""

import unittest
import numpy as np
from mdp_irrigation import SmartIrrigationMDP
from irrigation_solver import SmartIrrigationAdvisor


class TestSmartIrrigationMDP(unittest.TestCase):
    def setUp(self):
        self.mdp = SmartIrrigationMDP(
            temperature=35.0,
            water_availability="Medium",
            crop="Cotton at Flowering",
            gamma=0.90,
            epsilon=1e-5,
        )

    def test_state_space_dimensions(self):
        self.assertEqual(self.mdp.num_states, 10)
        self.assertEqual(self.mdp.num_moisture, 5)
        self.assertEqual(self.mdp.num_rain, 2)
        self.assertEqual(self.mdp.num_actions, 4)

    def test_state_encoding_decoding(self):
        for m in range(self.mdp.num_moisture):
            for r in range(self.mdp.num_rain):
                s = self.mdp.encode_state(m, r)
                dec_m, dec_r = self.mdp.decode_state(s)
                self.assertEqual((m, r), (dec_m, dec_r))

    def test_transition_probability_stochasticity(self):
        """Every row in P(s, a, :) must sum to exactly 1.0 (valid probability distribution)."""
        for s in range(self.mdp.num_states):
            for a in range(self.mdp.num_actions):
                row_sum = np.sum(self.mdp.P[s, a, :])
                self.assertAlmostEqual(row_sum, 1.0, places=5)
                # No negative probabilities
                self.assertTrue(np.all(self.mdp.P[s, a, :] >= 0.0))

    def test_target_scenario_mapping(self):
        """Test that 25% moisture and 'Rain expected' maps to State 3."""
        s = self.mdp.map_inputs_to_state(25.0, "Rain expected")
        self.assertEqual(s, 3)
        m_idx, r_idx = self.mdp.decode_state(s)
        self.assertEqual(m_idx, 1)  # Dry (20-35%)
        self.assertEqual(r_idx, 1)  # Rain Expected

    def test_value_iteration_convergence(self):
        V, policy, q_table, iterations = self.mdp.solve_value_iteration()
        self.assertGreater(iterations, 0)
        self.assertLess(iterations, 1000)
        self.assertEqual(len(V), 10)
        self.assertEqual(len(policy), 10)
        self.assertEqual(q_table.shape, (10, 4))

    def test_target_recommendation_low_irrigation(self):
        """
        Critical requirement:
        For State 3 (Dry 25% moisture, Rain Expected, 35 C, Medium Water, Cotton at Flowering),
        Value Iteration must recommend Low Irrigation (10L).
        """
        advisor = SmartIrrigationAdvisor(
            temperature=35.0,
            water_availability="Medium",
            crop="Cotton at Flowering",
        )
        result = advisor.advise(
            soil_moisture_pct=25.0,
            temperature=35.0,
            rain_forecast="Rain expected",
            water_availability="Medium",
            crop="Cotton at Flowering",
        )

        self.assertEqual(result["state_index"], 3)
        self.assertEqual(result["recommended_volume_liters"], 10)
        self.assertEqual(result["recommended_action"], "Low Irrigation (10L)")

        # Verify Q(10L) > Q(0L), Q(25L), Q(40L)
        q_vals = result["q_values"]
        self.assertGreater(q_vals["Low Irrigation (10L)"], q_vals["No Irrigation (0L)"])
        self.assertGreater(q_vals["Low Irrigation (10L)"], q_vals["Medium Irrigation (25L)"])
        self.assertGreater(q_vals["Low Irrigation (10L)"], q_vals["High Irrigation (40L)"])

    def test_waterlogged_state_no_irrigation(self):
        """When soil is already waterlogged, optimal action must be No Irrigation (0L)."""
        V, policy, _, _ = self.mdp.solve_value_iteration()
        # State 8: Waterlogged, No Rain
        self.assertEqual(policy[8], 0)
        # State 9: Waterlogged, Rain Expected
        self.assertEqual(policy[9], 0)


if __name__ == "__main__":
    unittest.main()
