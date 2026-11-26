# College Student Academic Early-Warning System (AI-Mentor)

An AI-driven academic early-warning advisory system that analyzes early-semester indicators to predict whether college students are on track to **Pass** ($G3 \ge 10$) or **Fail** ($G3 < 10$) weeks before final examinations, enabling proactive and targeted mentoring interventions.

---

## 📌 Project Overview

Academic attrition and course failures frequently stem from issues that manifest in the initial weeks of a semester. Traditional remediation only happens after final grades are posted—when it is too late.

This system provides academic advisors with an **Early-Warning AI Engine** that evaluates:
- **Academic habits**: Weekly study time (`studytime`), past failures (`failures`), lecture absences (`absences`).
- **Socio-demographic context**: Mother's education (`Medu`), Father's education (`Fedu`).
- **Lifestyle & wellbeing**: Free time (`freetime`), socializing (`goout`), health status (`health`).
- **Early-semester assessments**: Quiz 1 / Exam 1 (`G1`), Mid-term evaluation (`G2`).

The system implements and benchmarks four core AI classification algorithms:
1. **k-Nearest Neighbors (k-NN)**
2. **Decision Tree Classifier**
3. **Gaussian Naive Bayes**
4. **Perceptron**

Both **from-scratch NumPy implementations** and **Scikit-Learn benchmark baselines** are included and verified.

---

## 📊 Dataset Specification

The project uses a structured benchmark dataset modeled after the UCI Student Performance benchmark, reflecting 600 college student academic records:

| Feature | Type | Range / Categories | Description |
| :--- | :--- | :--- | :--- |
| `studytime` | Categorical / Ordinal | `1` to `4` | Weekly study time (`1`: <2h, `2`: 2-5h, `3`: 5-10h, `4`: >10h) |
| `failures` | Discrete | `0` to `4` | Number of past course failures |
| `absences` | Continuous | `0` to `32` | Number of missed lecture/lab hours |
| `Medu` | Categorical / Ordinal | `0` to `4` | Mother's education (`0`: None, `4`: Higher Education) |
| `Fedu` | Categorical / Ordinal | `0` to `4` | Father's education (`0`: None, `4`: Higher Education) |
| `freetime` | Scale | `1` to `5` | Free time after class (`1`: Low, `5`: High) |
| `goout` | Scale | `1` to `5` | Frequency of going out with peers |
| `health` | Scale | `1` to `5` | Current health status |
| `G1` | Continuous | `0` to `20` | Early-semester evaluation grade |
| `G2` | Continuous | `0` to `20` | Mid-semester examination grade |
| **`Pass_Fail`** | **Binary Target** | **`0` or `1`** | **`1`: Pass ($G3 \ge 10$) \| `0`: Fail / At-Risk ($G3 < 10$)** |

---

## 🧠 Machine Learning Models

### 1. k-Nearest Neighbors (k-NN)
- Classifies a student based on the majority label of their $k$ closest neighbors in standardized feature space using Euclidean distance.
- Effective for identifying cohorts with similar study patterns and academic histories.

### 2. Decision Tree Classifier
- Recursive binary splitting optimizing **Gini Impurity**:
  $$Gini(D) = 1 - \sum_{i=1}^{C} p_i^2$$
- Highly interpretable for academic advisors, directly revealing decision rules (e.g., threshold conditions on $G2$, $G1$, and absences).

### 3. Gaussian Naive Bayes
- Computes posterior probabilities using Bayes' Theorem under conditional independence assumptions:
  $$P(C_k \mid X) \propto P(C_k) \prod_{j=1}^{d} P(x_j \mid C_k)$$
- Demonstrates exceptional sensitivity to identifying failing students (100% recall on the at-risk class).

### 4. Perceptron
- Linear decision boundary classifier trained via the classical Rosenblatt delta update rule:
  $$w \leftarrow w + \eta (y - \hat{y}) x$$
  $$b \leftarrow b + \eta (y - \hat{y})$$
- Evaluates linear separability between passing and at-risk students following standard score scaling.

---

## 📈 Experimental Results & Model Comparison

Evaluated on a 25% stratified holdout test set (150 students: 130 Pass, 20 Fail):

| Model | Accuracy (%) | Precision | Recall (Pass) | F1-Score | At-Risk Recall (Fail Detection) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Perceptron (Custom)** | **96.00%** | **0.9627** | **0.9923** | **0.9773** | **75.0%** (15/20) |
| **Naive Bayes (Custom)** | **95.33%** | **1.0000** | **0.9462** | **0.9723** | **100.0%** (20/20) |
| **Decision Tree (Custom)** | **94.00%** | **0.9618** | **0.9692** | **0.9655** | **75.0%** (15/20) |
| **k-NN (Custom)** | **90.00%** | **0.9078** | **0.9846** | **0.9446** | **35.0%** (7/20) |
| *Perceptron (Scikit-Learn)* | 96.00% | 0.9921 | 0.9615 | 0.9766 | 95.0% (19/20) |
| *Naive Bayes (Scikit-Learn)* | 95.33% | 1.0000 | 0.9462 | 0.9723 | 100.0% (20/20) |
| *Decision Tree (Scikit-Learn)* | 95.33% | 0.9624 | 0.9846 | 0.9734 | 75.0% (15/20) |
| *k-NN (Scikit-Learn)* | 90.00% | 0.9078 | 0.9846 | 0.9446 | 35.0% (7/20) |

### Key Findings:
- **Best Model for Fail Detection**: **Gaussian Naive Bayes** achieved **100% recall on at-risk students**, capturing all 20 failing students without a single false negative. In an academic early-warning context, missing an at-risk student is the costliest error.
- **Top Overall Accuracy**: **Perceptron** achieved **96.00% accuracy**, demonstrating that normalized academic indicators create a distinct linear separation between pass and fail cohorts.
- **Explainability**: **Decision Tree** provides transparent rule-based thresholds that counselors can explain directly to students.

Visual performance charts and confusion matrices are generated in `results/`:
- `results/model_comparison_metrics.png`
- `results/confusion_matrices.png`

---

## 🎯 Targeted Mentoring Intervention Protocol

Based on model predictions, the early-warning system triggers tiered interventions 4–6 weeks prior to final exams:

| Risk Tier | Indicator Profile | Intervention Action Plan |
| :--- | :--- | :--- |
| **High Risk (Fail Predicted)** | $G1 < 10, G2 < 10$, failures $\ge 1$, absences $> 8$ | Mandatory 1-on-1 faculty mentoring, prerequisite knowledge tutoring, weekly check-ins, parental consultation. |
| **Moderate Risk** | $G1 \approx 10$, absences $5-8$, study time $< 2$h | Peer tutoring groups, study habit coaching, time management workshop. |
| **Low Risk (On Track)** | $G1 \ge 12, G2 \ge 12$, low absences | Standard milestone monitoring and encouragement for honors/extracurriculars. |

---

## 📁 Repository Structure

```
AI-Mentor/
├── data/
│   └── student_academic_records.csv   # Synthesized 600-student dataset
├── results/
│   ├── model_comparison_metrics.csv   # Exported benchmark metrics
│   ├── model_comparison_metrics.png   # Performance comparison bar chart
│   └── confusion_matrices.png         # Multi-model confusion matrix grid
├── src/
│   ├── __init__.py
│   ├── custom_models.py               # Pure Python/NumPy k-NN, Decision Tree, Naive Bayes, Perceptron
│   ├── data_loader.py                 # Data loading, indicator selection, StandardScaler pipeline
│   └── evaluate.py                    # Accuracy, Precision, Recall, F1, Specificity, Confusion Matrix
├── generate_dataset.py                # Standalone dataset generator
├── train_and_compare.py               # Main training, benchmark comparison & plot generation script
├── predict_student.py                 # Interactive early-warning CLI advisor for individual students
├── requirements.txt                   # Project dependencies
└── README.md                          # Comprehensive documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/varshith1708/AI-Mentor.git
cd AI-Mentor
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Model Training & Benchmark Comparison
```bash
python train_and_compare.py
```
This will:
- Load/generate the student dataset.
- Train all custom and Scikit-Learn models.
- Print detailed metric evaluation reports and comparison tables.
- Save comparison charts and CSV reports to `results/`.

### 4. Run Single Student Early-Warning Advisory CLI
Run a demonstration assessment on a high-risk sample student:
```bash
python predict_student.py
```

Or pass custom student indicators:
```bash
python predict_student.py --studytime 1 --failures 2 --absences 12 --Medu 2 --Fedu 2 --freetime 4 --goout 4 --health 3 --G1 7 --G2 8
```

Sample Advisor Output:
```text
=================================================================
 ACADEMIC EARLY-WARNING ADVISORY REPORT
=================================================================
 Student Indicators:
   - studytime   : 1.0
   - failures    : 2.0
   - absences    : 12.0
   - Medu        : 2.0
   - Fedu        : 2.0
   - freetime    : 4.0
   - goout       : 4.0
   - health      : 3.0
   - G1          : 7.0
   - G2          : 8.0
-----------------------------------------------------------------
 Evaluation Status : AT RISK OF FAILING (G3 < 10)
 Risk Classification: HIGH RISK - EARLY WARNING TRIGGERED
-----------------------------------------------------------------
 Targeted Mentoring Recommendations:
   * [CRITICAL] Enroll in mandatory faculty-led remedial study sessions.
   * [ATTENDANCE] High absences detected (12.0). Schedule counseling check-in.
   * [STUDY HABIT] Structured study schedule required: aim for at least 5-10 hours/week.
   * [ACADEMIC DEFICIT] Early assessments below threshold (G1=7.0, G2=8.0). Assign senior student peer tutor.
   * [REMEDIATION] Past failures noted (2.0). Conduct prerequisite knowledge review.
=================================================================
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
