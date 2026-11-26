import numpy as np
import pandas as pd
from scipy import stats
from config import Config
from services.dataset_service import load_dataset

class StatisticalEngine:
    """
    Statistical Hypothesis Testing Engine for AutoSense Nexus.
    Performs rigorous statistical significance testing (t-tests, Mann-Whitney U, 
    ANOVA, Chi-square tests) between vehicle sensor/symptom variables and fault classes.
    """
    
    def __init__(self):
        self.df = load_dataset()
        self.alpha = Config.ALPHA

    def run_all_variable_tests(self, target_fault=None):
        """
        Runs statistical tests across all continuous and symptom variables.
        If target_fault is specified, evaluates one-vs-rest association for that fault.
        Otherwise evaluates multi-class ANOVA and Chi-Square tests.
        """
        df = self.df
        results = []
        
        continuous_vars = [
            'battery_voltage', 'alternator_voltage', 'engine_rpm',
            'engine_temperature', 'coolant_temperature', 'oil_pressure'
        ]
        
        symptom_vars = Config.SYMPTOMS
        
        # 1. Continuous Variables
        for var in continuous_vars:
            if target_fault and target_fault in Config.FAULTS:
                group_fault = df[df['fault'] == target_fault][var]
                group_other = df[df['fault'] != target_fault][var]
                
                # Check normality for test selection
                _, norm_p = stats.shapiro(group_fault.sample(min(50, len(group_fault))))
                
                if norm_p > 0.05:
                    # Two-sample Independent Student's t-test
                    stat, p_val = stats.ttest_ind(group_fault, group_other, equal_var=False)
                    test_name = "Welch's t-test"
                    rationale = f"Compared continuous variable '{var}' for target fault '{target_fault}' vs other states using Welch's t-test."
                else:
                    # Non-parametric Mann-Whitney U test
                    stat, p_val = stats.mannwhitneyu(group_fault, group_other, alternative='two-sided')
                    test_name = "Mann-Whitney U Test"
                    rationale = f"Non-parametric rank sum test used as sensor values show skewed distributions."
            else:
                # One-Way ANOVA across all fault categories
                fault_groups = [group[var].values for _, group in df.groupby('fault')]
                stat, p_val = stats.f_oneway(*fault_groups)
                test_name = "One-Way ANOVA"
                rationale = f"Evaluated mean differences of '{var}' across all 8 vehicle fault categories."

            is_sig = bool(p_val < self.alpha)
            results.append({
                'variable': var,
                'variable_label': var.replace('_', ' ').title(),
                'target_fault': target_fault or 'ALL_FAULTS',
                'test_type': test_name,
                'statistic': round(float(stat), 4),
                'p_value': float(p_val),
                'p_value_formatted': f"{p_val:.4e}" if p_val < 0.0001 else f"{p_val:.4f}",
                'alpha': self.alpha,
                'is_significant': is_sig,
                'significance_status': "STATISTICALLY SIGNIFICANT" if is_sig else "NOT SIGNIFICANT",
                'rationale': rationale
            })
            
        # 2. Binary Symptom Variables (Chi-Square Test of Independence)
        for sym in symptom_vars:
            if target_fault and target_fault in Config.FAULTS:
                contingency = pd.crosstab(df[sym], df['fault'] == target_fault)
            else:
                contingency = pd.crosstab(df[sym], df['fault'])
                
            chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
            is_sig = bool(p_val < self.alpha)
            
            results.append({
                'variable': sym,
                'variable_label': sym.replace('_', ' ').title(),
                'target_fault': target_fault or 'ALL_FAULTS',
                'test_type': "Chi-Square Test (χ²)",
                'statistic': round(float(chi2), 4),
                'p_value': float(p_val),
                'p_value_formatted': f"{p_val:.4e}" if p_val < 0.0001 else f"{p_val:.4f}",
                'alpha': self.alpha,
                'is_significant': is_sig,
                'significance_status': "STATISTICALLY SIGNIFICANT" if is_sig else "NOT SIGNIFICANT",
                'rationale': f"Evaluated categorical association between symptom '{sym}' and vehicle fault classes using contingency table."
            })
            
        return results

    def get_significant_variables_for_evidence(self, inputs):
        """
        Determines which entered user variables show statistically significant deviation 
        or association with potential vehicle faults.
        """
        significant_items = []
        all_tests = self.run_all_variable_tests()
        
        for test in all_tests:
            var = test['variable']
            if test['is_significant']:
                user_val = inputs.get(var)
                significant_items.append({
                    'variable': var,
                    'label': test['variable_label'],
                    'value': user_val,
                    'p_value': test['p_value_formatted'],
                    'test_type': test['test_type'],
                    'impact': 'HIGH' if test['p_value'] < 0.001 else 'MODERATE'
                })
                
        return significant_items

    @staticmethod
    def get_statistical_methodology_explanation():
        return {
            'core_principle': (
                "Statistical hypothesis testing evaluates whether observed vehicle sensor/symptom data "
                "differ significantly from standard operating baseline conditions under the null hypothesis (H₀)."
            ),
            'p_value_definition': (
                "A p-value measures the probability of obtaining test results at least as extreme as the observed "
                "results, assuming the null hypothesis (no association/difference) is true. "
                "p < 0.05 indicates statistical significance."
            ),
            'bayesian_distinction': (
                "CRITICAL DISTINCTION: Statistical hypothesis testing identifies WHICH variables show significant "
                "associations with vehicle faults. The Bayesian Network then propagates evidence from these "
                "variables to compute the actual posterior fault probabilities P(Fault | Evidence)."
            )
        }
