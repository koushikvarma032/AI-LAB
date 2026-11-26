# Smart Irrigation System in Gujarat: Policy-Based Decision Making

An AI-driven decision-making system using a **Markov Decision Process (MDP)** and **Value Iteration** for precision agriculture in Gujarat, India. Designed specifically for **Cotton at the Flowering Stage** in semi-arid black soil, the policy balances soil moisture requirements, ambient temperature (35°C), precipitation forecasts, and groundwater conservation to avoid waterlogging and drought stress.

---

## Problem Scenario

A farmer in Gujarat inputs real-time field telemetry:
- **Crop**: Cotton at Flowering stage
- **Soil Moisture**: 25% (Dry)
- **Ambient Temperature**: 35°C (High Evapotranspiration)
- **Rain Forecast**: 'Rain expected'
- **Water Availability**: 'Medium' (Regulated groundwater reserves)

### Key Challenge
Cotton during its flowering and boll-formation phase is sensitive to both moisture stress and excess water:
1. **Drought Stress**: If rain fails or is delayed under 35°C heat, un-irrigated dry soil drops into wilting range (<20%), triggering square and boll shedding.
2. **Waterlogging**: Gujarat's heavy black cotton soil has low drainage. Applying heavy (40L) or medium (25L) irrigation before expected rainfall saturates the root zone (>80%), causing root hypoxia and flower abortion.
3. **Groundwater Scarcity**: Pumping excessive water depletes critical aquifers and incurs unnecessary operational costs.

### The AI Recommendation
Running **Value Iteration** over the 10-state MDP identifies **Low Irrigation (10L)** as the optimal policy. Low irrigation provides a protective moisture cushion against high heat while leaving sufficient soil pore capacity to absorb incoming rains without waterlogging penalties.

---

## Mathematical Formulation

### 1. State Space
The state space consists of 5 Moisture Levels x 2 Weather Forecasts = 10 Discrete States:

- **Soil Moisture Levels (m)**:
  - m=0: Very Dry (<20%)
  - m=1: Dry (20% - 35%) — *(Current: 25%)*
  - m=2: Optimal (35% - 60%)
  - m=3: Wet (60% - 80%)
  - m=4: Waterlogged (>80%)
- **Weather / Rain Forecasts (r)**:
  - r=0: No Rain Expected
  - r=1: Rain Expected — *(Current: Rain expected)*

State index: `s = m * 2 + r` (s from 0 to 9)

### 2. Action Space
- Action 0: 0L (No Irrigation)
- Action 1: 10L (Low Irrigation)
- Action 2: 25L (Medium Irrigation)
- Action 3: 40L (High Irrigation)

### 3. Transition Probability Model P(s' | s, a)
State transitions model environmental dynamics under Gujarat's climatic conditions:
- **Precipitation Realization**: If r=1 ('Rain expected'), rain occurs with 65% probability.
- **Evapotranspiration (ET)**: At 35°C, high evapotranspiration induces moisture loss when rain is absent.
- **Irrigation Effect**: Irrigation volume raises soil moisture levels.
- **Weather Forecast Transition**: Modeled via a 2-state Markov chain.

### 4. Reward Function R(s, a, s')
The reward function reflects crop health and water conservation:
- **Crop Moisture Reward**:
  - Optimal (m'=2): +25.0
  - Wet (m'=3): +4.0
  - Dry (m'=1): -7.0
  - Very Dry (m'=0): -22.0
  - Waterlogged (m'=4): -26.0
- **Water Conservation Cost** under 'Medium' availability:
  - 0L: 0.0
  - 10L: -1.2
  - 25L: -3.8
  - 40L: -7.5

### 5. Value Iteration Algorithm
The optimal value function V*(s) is computed via the Bellman Optimality Equation:
`V_{k+1}(s) = max_a sum_{s'} P(s' | s, a) [ R(s, a, s') + gamma * V_k(s') ]`

Iterated until convergence (|V_{k+1} - V_k| < epsilon).

---

## Optimal Policy & Q-Value Results

Running the Value Iteration algorithm yields convergence in 112 iterations:

| State | Moisture Level | Rain Forecast | Q(0L) | Q(10L) | Q(25L) | Q(40L) | V*(s) | Optimal Action |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|
| 0 | Very Dry (<20%) | No Rain Expected | -2.03 | +5.69 | +18.66 | +19.99 | +19.99 | High Irrigation (40L) |
| 1 | Very Dry (<20%) | Rain Expected | +4.61 | +15.08 | +16.73 | -3.99 | +16.73 | Medium Irrigation (25L) |
| 2 | Dry (20-35%) | No Rain Expected | +8.47 | +21.26 | +23.69 | -5.47 | +23.69 | Medium Irrigation (25L) |
| 3 | Dry (20-35%) | Rain Expected | +18.34 | +19.33 | -0.29 | -31.31 | +19.33 | Low Irrigation (10L) |
| 4 | Optimal (35-60%) | No Rain Expected | +24.93 | +26.29 | -1.77 | -36.81 | +26.29 | Low Irrigation (10L) |
| 5 | Optimal (35-60%) | Rain Expected | +20.92 | +2.31 | -27.61 | -46.51 | +20.92 | No Irrigation (0L) |
| 6 | Wet (60-80%) | No Rain Expected | +27.94 | +0.83 | -33.11 | -41.54 | +27.94 | No Irrigation (0L) |
| 7 | Wet (60-80%) | Rain Expected | +0.44 | -25.01 | -42.81 | -48.43 | +0.44 | No Irrigation (0L) |
| 8 | Waterlogged (>80%) | No Rain Expected | -2.55 | -30.51 | -37.84 | -41.54 | -2.55 | No Irrigation (0L) |
| 9 | Waterlogged (>80%) | Rain Expected | -28.09 | -40.21 | -44.73 | -48.43 | -28.09 | No Irrigation (0L) |

### State 3 (Farmer Scenario)
- **Soil Moisture**: 25% -> State 3
- **Rain Forecast**: Rain expected -> State 3
- **Q-Values**:
  - Q(s=3, a=0L) = 18.34
  - **Q(s=3, a=10L) = 19.33 (Optimal)**
  - Q(s=3, a=25L) = -0.29
  - Q(s=3, a=40L) = -31.31

#### Why Low Irrigation (10L) is Selected:
1. **Avoids Waterlogging Penalty**: If 25L or 40L is applied and rain falls, moisture reaches level 4 (Waterlogged), triggering a severe -26.0 penalty.
2. **Buffers Against Heat & Rain Delay**: If 0L is applied and rain is delayed or light, 35°C heat drives the soil into drought (<20%).
3. **Conserves Groundwater**: 10L preserves precious water under 'Medium' availability.

---

## Repository Structure

```
├── mdp_irrigation.py       # Core MDP formulation, transition models & Value Iteration solver
├── irrigation_solver.py    # Advisory engine mapping environmental inputs to policy decisions
├── main.py                 # Main executable demonstration with formatted telemetry & policy tables
├── test_irrigation.py      # Unit test suite verifying MDP stochasticity, convergence, & decisions
├── requirements.txt        # Dependencies (numpy, tabulate)
├── .gitignore              # Standard Python ignore rules
└── README.md               # Documentation
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Decision-Making System
```bash
python main.py
```

### 3. Run Unit Tests
```bash
python -m unittest test_irrigation.py
```
