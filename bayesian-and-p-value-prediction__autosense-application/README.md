# AutoSense Nexus — Intelligent Vehicle Fault Detection

### **Probabilistic Vehicle Intelligence Engine Using Statistical Hypothesis Testing + Bayesian Graphical Networks**

AutoSense Nexus is an academic & research AI web application for detecting probable vehicle faults from sensor readings and observed symptoms.

The system combines two complementary methodologies:
1. **Statistical Hypothesis Testing using p-values** (SciPy: Welch's t-test, Mann-Whitney U, ANOVA, Chi-Square tests) to identify variables with statistically significant associations.
2. **Bayesian Network Probabilistic Graphical Modeling** (pgmpy DiscreteBayesianNetwork & VariableElimination) to compute exact posterior fault probabilities \(P(\text{Fault} \mid \text{Evidence})\).

---

## 🚀 Key Features

- **Futuristic Automotive Command Center UI:** Dark premium engineering dashboard with glassmorphism, responsive telemetry badges, and interactive vehicle silhouette.
- **Dynamic Bayesian Inference:** Powered by `pgmpy`. Calculates 100% dynamic non-hardcoded posterior probabilities for 8 vehicle fault categories.
- **Statistical Significance Lab:** Rigorous hypothesis testing against significance level \(\alpha = 0.05\) with clear p-value interpretation.
- **Multi-Step Diagnostic Pipeline:** Visual step-by-step processing animation (Data Validation $\rightarrow$ Statistical Analysis $\rightarrow$ p-values $\rightarrow$ Bayesian Propagation $\rightarrow$ Posterior Probabilities $\rightarrow$ Diagnosis).
- **Explainable AI Engine:** Natural language diagnostic rationales explaining *why* the system reached its conclusion without confusing p-values with causation probabilities.
- **Quantitative Evidence Map:** Leave-one-out Bayesian probability shift visualization showing exact variable importance percentages.
- **Interactive Probabilistic Graph:** Vis.js powered network DAG visualizer with node selection, state inspection, and Tabular CPT browser.
- **Vehicle Telemetry Data Explorer:** Interactive dataset browser with search, missing-value analysis, and Chart.js histograms.
- **Scenario Lab:** 6 preconfigured real-world demonstration scenarios (Weak Battery, Alternator Issue, Overheating, Low Oil Pressure, Starter Motor, Ignition Misfire) for college presentations.
- **Before vs After Repair Comparison:** Side-by-side diagnostic comparison tool to verify repair effectiveness and probability deltas.
- **ReportLab PDF Generator:** Downloadable diagnostic report formatted with telemetry tables, p-values, Bayesian posteriors, and disclaimers.
- **Model Performance Metrics:** 20% test split validation evaluating Accuracy, Precision, Recall, F1-Score, and a Multi-Class Confusion Matrix.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Flask 3.x
- **Data Science & Math:** Pandas, NumPy, SciPy, Statsmodels, scikit-learn
- **Bayesian Modeling:** pgmpy (`DiscreteBayesianNetwork`, `BayesianEstimator`, `VariableElimination`)
- **PDF Generation:** ReportLab 5.0
- **Testing:** pytest 9.0
- **Frontend UI:** HTML5, Jinja2, Tailwind CSS 3.x, FontAwesome 6
- **Visualizations:** Vis.js Network, Chart.js

---

## 📂 Project Architecture

```text
autosense_nexus/
│
├── app.py                      # Flask main entrypoint
├── config.py                   # Configuration parameters (paths, alpha, thresholds)
├── requirements.txt            # Dependency list
├── README.md                   # System documentation
│
├── data/
│   └── vehicle_fault_data.csv  # 1400 realistic synthetic vehicle records
│
├── models/
│   └── bayesian_network.py     # pgmpy Bayesian Network DAG & CPT trainer
│
├── services/
│   ├── dataset_service.py       # Data loader & synthetic dataset generator
│   ├── statistical_service.py   # SciPy/Statsmodels hypothesis tests (t-test, χ², ANOVA)
│   ├── bayesian_service.py      # pgmpy inference singleton & graph data provider
│   ├── diagnosis_service.py     # 7-step diagnostic pipeline & evidence map calculation
│   ├── preprocessing_service.py # Input validation & continuous sensor discretization
│   ├── evaluation_service.py    # Test split evaluation metrics (Accuracy, F1, Confusion Matrix)
│   └── report_service.py        # ReportLab PDF report generator
│
├── routes/
│   ├── main_routes.py          # Dashboard (/), scenarios (/scenarios), fault library (/fault-library)
│   ├── diagnostic_routes.py    # Live Diagnostics (/diagnostics), API POST /api/diagnose, /api/compare
│   ├── statistical_routes.py   # Statistical Lab (/statistics), API POST /api/statistical-analysis
│   ├── bayesian_routes.py      # Bayesian Graph (/bayesian-network), API GET /api/bayesian-network
│   ├── data_routes.py          # Data Explorer (/data-explorer), API GET /api/dataset-summary
│   └── report_routes.py        # API POST /api/generate-report
│
├── templates/                  # Jinja2 UI templates
│   ├── base.html
│   ├── dashboard.html
│   ├── diagnostics.html
│   ├── statistics.html
│   ├── bayesian.html
│   ├── data_explorer.html
│   ├── scenarios.html
│   ├── fault_library.html
│   ├── compare.html
│   └── evaluation.html
│
├── static/                     # Assets, custom CSS, and JS controllers
│   ├── css/style.css
│   └── js/ (dashboard.js, diagnostics.js, bayesian.js, statistics.js, data_explorer.js, compare.js)
│
├── tests/                      # Automated Pytest suite
│   ├── test_statistics.py
│   ├── test_bayesian.py
│   ├── test_diagnosis.py
│   └── test_routes.py
│
└── docs/
    └── methodology.md          # Comprehensive mathematical documentation
```

---

## 🚘 Supported Vehicle Faults

1. **Battery Failure / Degradation**
2. **Alternator Charging Failure**
3. **Starter Motor Failure**
4. **Engine Thermal Overheating**
5. **Low Oil Pressure Hazard**
6. **Ignition / Spark Plug Misfire**
7. **Cooling System Component Failure**
8. **No Fault (Normal Operating Vehicle)**

---

## ⚡ Quick Start & Installation

### 1. Clone & Navigate to Project Directory
```bash
cd autosense_nexus
```

### 2. Create and Activate Virtual Environment
**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
python -m pytest tests/
```

Expected output: `18 passed in ~7s`.

---

## 📡 Key API Endpoints

- `POST /api/diagnose` — Accepts sensor reading JSON, executes diagnostic pipeline, returns posterior probabilities & evidence map.
- `POST /api/statistical-analysis` — Runs SciPy hypothesis tests against \(\alpha = 0.05\).
- `GET  /api/bayesian-network` — Returns Vis.js network graph topology (nodes, edges).
- `GET  /api/bayesian-cpd/<node_name>` — Returns Tabular CPT for specified node.
- `GET  /api/dataset-summary` — Returns record count, column ranges, and missing value metrics.
- `POST /api/compare` — Compares two evidence sets (Before vs After repair) and returns probability deltas.
- `POST /api/generate-report` — Generates binary ReportLab PDF diagnostic report for download.

---

## 🛡️ Safety Disclaimer

> **AutoSense Nexus** is an educational and decision-support prototype. Its predictions are probabilistic and should not be used as the sole basis for vehicle repair or safety decisions. Always verify suspected faults using appropriate diagnostic equipment and a qualified automotive professional.
