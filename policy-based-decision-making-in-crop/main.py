#!/usr/bin/env python3
"""
Main entry point for Smart Irrigation Decision-Making System in Gujarat.

Demonstrates the scenario:
- Soil Moisture: 25% (Dry)
- Temperature: 35 deg C
- Rain Forecast: 'Rain expected'
- Water Availability: 'Medium'
- Crop: 'Cotton at Flowering'
- AI Engine: Value Iteration over 10-State Markov Decision Process (MDP)
- Recommendation: Low Irrigation (10L)
"""

import sys
from mdp_irrigation import SmartIrrigationMDP
from irrigation_solver import SmartIrrigationAdvisor

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


def print_table(headers, rows):
    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="fancy_grid", floatfmt=".2f"))
    else:
        # Fallback pure-python table formatter
        widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                widths[i] = max(widths[i], len(str(val)))
        header_str = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        separator = "-+-".join("-" * widths[i] for i in range(len(headers)))
        print(header_str)
        print(separator)
        for row in rows:
            print(" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)))


def main():
    print("\n" + "=" * 80)
    print("   SMART IRRIGATION SYSTEM IN GUJARAT: MDP POLICY-BASED DECISION MAKING   ")
    print("      Optimizing Cotton Yields & Groundwater Preservation in Vertisols     ")
    print("=" * 80 + "\n")

    # 1. Farmer Input Parameters
    soil_moisture = 25.0
    temperature = 35.0
    rain_forecast = "Rain expected"
    water_availability = "Medium"
    crop = "Cotton at Flowering"

    print("[*] 1. FARMER TELEMETRY & INPUT CONDITIONS:")
    print(f"    - Crop & Growth Stage     : {crop}")
    print(f"    - Current Soil Moisture   : {soil_moisture}% (Dry Soil: Level 1)")
    print(f"    - Ambient Temperature     : {temperature}°C (High Evapotranspiration)")
    print(f"    - Rain Forecast           : {rain_forecast}")
    print(f"    - Water Availability      : {water_availability} (Groundwater Preservation Active)")
    print()

    # 2. Initialize MDP & Solve
    print("[*] 2. RUNNING VALUE ITERATION OVER 10-STATE MDP...")
    mdp = SmartIrrigationMDP(
        temperature=temperature,
        water_availability=water_availability,
        crop=crop,
        gamma=0.90,
        epsilon=1e-5,
    )
    V, policy, q_table, iterations = mdp.solve_value_iteration()
    print(f"    [+] Bellman Optimality Equation converged in {iterations} iterations.")
    print(f"    [+] State Space: 5 Moisture Levels x 2 Rain Forecasts = 10 States.")
    print(f"    [+] Action Space: 4 Actions [0L, 10L, 25L, 40L].\n")

    # 3. Complete Policy Table Display
    print("[*] 3. COMPLETE MDP OPTIMAL POLICY & Q-VALUE TABLE:")
    headers = ["State", "Moisture Level", "Rain Forecast", "Q(0L)", "Q(10L)", "Q(25L)", "Q(40L)", "V*(s)", "Optimal Action"]
    rows = []
    current_state_idx = mdp.map_inputs_to_state(soil_moisture, rain_forecast)

    for s in range(mdp.num_states):
        m_idx, r_idx = mdp.decode_state(s)
        m_name = mdp.MOISTURE_LEVELS[m_idx]
        r_name = mdp.RAIN_FORECASTS[r_idx]
        best_a = int(policy[s])
        action_name = mdp.ACTION_NAMES[best_a]

        marker = "-> [TARGET]" if s == current_state_idx else f"   State {s}"
        row = [
            marker,
            m_name,
            r_name,
            f"{q_table[s, 0]:.2f}",
            f"{q_table[s, 1]:.2f}",
            f"{q_table[s, 2]:.2f}",
            f"{q_table[s, 3]:.2f}",
            f"{V[s]:.2f}",
            action_name,
        ]
        rows.append(row)

    print_table(headers, rows)
    print()

    # 4. Detailed Recommendation for the Farmer's State
    advisor = SmartIrrigationAdvisor(
        temperature=temperature,
        water_availability=water_availability,
        crop=crop,
    )
    result = advisor.advise(
        soil_moisture_pct=soil_moisture,
        temperature=temperature,
        rain_forecast=rain_forecast,
        water_availability=water_availability,
        crop=crop,
    )

    print("[*] 4. AI AGENT IRRIGATION RECOMMENDATION:")
    print("+" + "-" * 78 + "+")
    print(f"| RECOMMENDED ACTION : {result['recommended_action'].upper():<54} |")
    print(f"| RECOMMENDED VOLUME : {str(result['recommended_volume_liters']) + ' Liters':<54} |")
    print(f"| STATE VALUE V*(s)  : {result['expected_value_V']:<54.2f} |")
    print("+" + "-" * 78 + "+")
    print()

    print("[*] 5. AGRONOMIC & DECISION-THEORETIC RATIONALE:")
    print(result["explanation"])
    print("\n" + "=" * 80)
    print("System execution completed successfully.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
