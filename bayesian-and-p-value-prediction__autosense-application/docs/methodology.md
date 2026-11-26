# AutoSense Nexus — Mathematical & Statistical Methodology

This document outlines the rigorous mathematical, statistical, and probabilistic graphical model foundations underlying **AutoSense Nexus**.

---

## 1. System Architecture Overview

AutoSense Nexus combines two distinct mathematical frameworks:

```text
              VEHICLE SENSOR TELEMETRY & SYMPTOMS
                              ↓
                  DATA VALIDATION & BINNING
                              ↓
              STATISTICAL HYPOTHESIS TESTING
             (SciPy: t-test, Mann-Whitney U, χ²)
                              ↓
                  CALCULATE P-VALUES (α = 0.05)
                              ↓
             IDENTIFY SIGNIFICANT DEVIANT VARIABLES
                              ↓
               PGMPY BAYESIAN NETWORK (DAG)
            (Conditional Probability Tables CPDs)
                              ↓
              EVIDENCE PROPAGATION & INFERENCE
                 (VariableElimination Engine)
                              ↓
             DYNAMIC FAULT POSTERIOR PROBABILITIES
                    P(Fault | Evidence)
                              ↓
              EXPLAINABLE DIAGNOSIS & EVIDENCE MAP
```

---

## 2. Statistical Analysis & Hypothesis Testing (Method 1)

Statistical hypothesis testing determines whether observed vehicle sensor/symptom distributions show statistically significant associations with vehicle fault categories.

### 2.1 Formulation of Hypotheses

For any vehicle variable \(X\) and fault category \(Y\):

- **Null Hypothesis (\(H_0\)):** There is no statistically significant association between vehicle variable \(X\) and fault category \(Y\) (the observed sample differences are due to random noise).
- **Alternative Hypothesis (\(H_1\)):** There is a statistically significant association between variable \(X\) and fault category \(Y\).

### 2.2 Test Selection Criteria

AutoSense Nexus dynamically selects test types based on variable types and distribution assumptions:

1. **Welch's Two-Sample Independent t-test:**
   Used for continuous sensor variables (e.g., `battery_voltage`) comparing samples for a specific fault group vs other fault groups when distributions are approximately normal:
   $$t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

2. **Mann-Whitney U Test:**
   Non-parametric rank-sum test utilized when continuous sensor variables exhibit skewed or non-normal distributions:
   $$U = n_1 n_2 + \frac{n_1(n_1+1)}{2} - R_1$$

3. **One-Way ANOVA (Analysis of Variance):**
   Evaluates continuous sensor variation across all multi-class fault categories simultaneously:
   $$F = \frac{\text{MS}_{between}}{\text{MS}_{within}}$$

4. **Pearson's Chi-Square Test of Independence (\(\chi^2\)):**
   Used for binary categorical symptom variables (e.g., `slow_cranking`, `dim_headlights`) against vehicle fault contingency tables:
   $$\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

### 2.3 Interpretation of p-values

- **Significance Threshold:** \(\alpha = 0.05\)
- **Decision Rule:**
  - If \(p < 0.05\): Reject \(H_0\). The variable is classified as **Statistically Significant**.
  - If \(p \ge 0.05\): Fail to reject \(H_0\).

> [!IMPORTANT]
> **Critical Distinction:** A p-value measures the probability of observing data as extreme as measured under \(H_0\). A p-value is **NOT** a prediction probability that a fault exists. Hypothesis testing identifies *which* variables are statistically significant, while the Bayesian Network computes *what* the fault probabilities are.

---

## 3. Bayesian Network & Probabilistic Inference (Method 2)

AutoSense Nexus uses a genuine Bayesian Graphical Network implemented in `pgmpy` to compute posterior probabilities given observed evidence.

### 3.1 Bayes' Theorem

The posterior probability of a vehicle fault \(F_i\) given observed evidence \(E = \{e_1, e_2, \dots, e_k\}\) is calculated as:

$$P(F_i \mid E) = \frac{P(E \mid F_i) \cdot P(F_i)}{P(E)} = \frac{P(E \mid F_i) \cdot P(F_i)}{\sum_{j} P(E \mid F_j) \cdot P(F_j)}$$

Where:
- \(P(F_i \mid E)\) is the **Posterior Probability** of fault \(F_i\).
- \(P(E \mid F_i)\) is the **Likelihood** of observing evidence \(E\) under fault \(F_i\).
- \(P(F_i)\) is the **Prior Probability** of fault \(F_i\).
- \(P(E)\) is the marginal probability of the evidence normalization constant.

### 3.2 Directed Acyclic Graph (DAG) Structure

The network topology connects node types:
- **Root Node:** `fault` (8 discrete states)
- **Discretized Sensor Nodes:** `battery_voltage_state`, `alternator_voltage_state`, `engine_temp_state`, `coolant_temp_state`, `oil_pressure_state`, `rpm_state`
- **Symptom Nodes:** `slow_cranking`, `hard_starting`, `dim_headlights`, `engine_noise`, `overheating_indicator`

CPDs (Tabular Conditional Probability Distributions) are learned directly from dataset records using `BayesianEstimator` with BDeu Dirichlet priors (Laplace smoothing) to prevent zero-frequency probabilities.

### 3.3 Exact Inference via Variable Elimination

Posterior queries \(P(\text{fault} \mid E)\) are computed using exact **Variable Elimination** in `pgmpy`:
1. Factors involving evidence variables are instantiated with observed states.
2. Intermediate non-query variables are marginalized out.
3. The remaining factor over `fault` is normalized so that \(\sum_{i} P(F_i \mid E) = 1.0\).

---

## 4. Quantitative Evidence Map Calculation

To explain which evidence observations contributed most heavily to a diagnosed fault \(F_{\text{top}}\), AutoSense Nexus calculates leave-one-out probability shifts:

$$\Delta P(e_m) = \left| P(F_{\text{top}} \mid E) - P(F_{\text{top}} \mid E \setminus \{e_m\}) \right|$$

Importance percentages are normalized:

$$\text{Importance}(e_m) = \frac{\Delta P(e_m)}{\sum_{j} \Delta P(e_j)} \times 100\%$$

This ensures that the visual Evidence Map reflects exact calculated Bayesian influence strengths rather than arbitrary hardcoded numbers.
