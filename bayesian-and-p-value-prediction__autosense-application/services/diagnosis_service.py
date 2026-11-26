import numpy as np
import pandas as pd
from config import Config
from services.preprocessing_service import validate_diagnostic_input, convert_inputs_to_bayesian_evidence
from services.statistical_service import StatisticalEngine
from services.bayesian_service import query_bayesian_diagnosis, get_bayesian_model

class DiagnosisEngine:
    """
    Core Diagnostic Pipeline for AutoSense Nexus.
    Executes: Data Validation -> Preprocessing -> Statistical Hypothesis Testing (p-values)
    -> Significant Variable Filter -> Bayesian Evidence Propagation -> Posterior Probabilities
    -> Fault Ranking -> Explainable Diagnosis -> Quantitative Evidence Map.
    """

    def __init__(self):
        self.stats_engine = StatisticalEngine()

    def process_diagnosis(self, raw_input_data):
        """
        Executes end-to-end diagnostic pipeline.
        Returns complete diagnostic result payload.
        """
        # Step 1: Validation
        is_valid, inputs, error_msg = validate_diagnostic_input(raw_input_data)
        if not is_valid:
            return {
                'success': False,
                'error': error_msg
            }
            
        # Step 2: Convert continuous/binary inputs to Bayesian evidence states
        bayesian_evidence = convert_inputs_to_bayesian_evidence(inputs)
        
        # Step 3: Statistical Analysis & P-Value calculation
        stat_results = self.stats_engine.run_all_variable_tests()
        significant_vars = [t for t in stat_results if t['is_significant']]
        
        # Step 4: Bayesian Network Evidence Propagation & Posterior Calculation
        posterior_probs = query_bayesian_diagnosis(bayesian_evidence)
        
        # Determine Top Fault and Alternative Hypotheses
        fault_list = list(posterior_probs.items())
        top_fault, top_prob = fault_list[0]
        alt_hypotheses = fault_list[1:]
        
        # Step 5: Explainable AI Synthesis ("Why did the system reach this conclusion?")
        explanations = self._generate_explanations(inputs, bayesian_evidence, top_fault, top_prob, significant_vars)
        
        # Step 6: Quantitative Evidence Map Calculation (Evidence Strength)
        evidence_map = self._calculate_evidence_importance(inputs, bayesian_evidence, top_fault)
        
        # Step 7: Format System Status Badges for Dashboard Visualization
        sensor_statuses = self._get_sensor_statuses(inputs)

        return {
            'success': True,
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'inputs': inputs,
            'bayesian_evidence': bayesian_evidence,
            'top_fault': top_fault,
            'top_fault_label': top_fault.replace('_', ' ').title(),
            'top_probability': round(top_prob * 100, 1),
            'top_probability_raw': top_prob,
            'posteriors': {k: round(v * 100, 1) for k, v in posterior_probs.items()},
            'alternative_hypotheses': [
                {'fault': k, 'label': k.replace('_', ' ').title(), 'probability': round(v * 100, 1)}
                for k, v in alt_hypotheses
            ],
            'statistical_summary': {
                'total_tests': len(stat_results),
                'significant_count': len(significant_vars),
                'alpha': Config.ALPHA,
                'significant_variables': [
                    {
                        'variable': t['variable'],
                        'label': t['variable_label'],
                        'test': t['test_type'],
                        'p_value': t['p_value_formatted'],
                        'significant': True
                    }
                    for t in significant_vars
                ]
            },
            'explanations': explanations,
            'evidence_map': evidence_map,
            'sensor_statuses': sensor_statuses,
            'disclaimer': Config.DISCLAIMER_TEXT
        }

    def _generate_explanations(self, inputs, evidence, top_fault, top_prob, significant_vars):
        """
        Synthesizes explainable, natural language diagnostic rationales.
        """
        reasons = []
        
        # Sensor specific observations
        if inputs['battery_voltage'] < 12.0:
            reasons.append(f"Battery voltage ({inputs['battery_voltage']} V) is below normal operating threshold (12.4 - 14.7 V).")
        elif inputs['battery_voltage'] > 14.7:
            reasons.append(f"Battery voltage ({inputs['battery_voltage']} V) is higher than expected baseline.")
            
        if inputs['alternator_voltage'] < 13.2:
            reasons.append(f"Alternator charging voltage ({inputs['alternator_voltage']} V) indicates inadequate alternator output (< 13.6 V).")
            
        if inputs['coolant_temperature'] > 98.0:
            reasons.append(f"Coolant temperature ({inputs['coolant_temperature']} °C) exceeds normal thermal limit (95.0 °C).")
            
        if inputs['engine_temperature'] > 100.0:
            reasons.append(f"Engine temperature ({inputs['engine_temperature']} °C) is abnormally elevated.")
            
        if inputs['oil_pressure'] < 25.0:
            reasons.append(f"Engine oil pressure ({inputs['oil_pressure']} PSI) is dangerously low (< 25.0 PSI).")
            
        if inputs['engine_rpm'] < 650:
            reasons.append(f"Engine idle speed ({inputs['engine_rpm']} RPM) indicates engine stalling or low cranking speed.")

        # Symptom observations
        if inputs.get('slow_cranking'):
            reasons.append("Slow engine cranking symptom was explicitly reported by user.")
        if inputs.get('dim_headlights'):
            reasons.append("Dim headlight illumination symptom observed during engine start.")
        if inputs.get('hard_starting'):
            reasons.append("Hard engine starting / extended cranking time reported.")
        if inputs.get('engine_noise'):
            reasons.append("Abnormal engine mechanical noise detected.")
        if inputs.get('overheating_indicator'):
            reasons.append("High temperature overheating warning indicator active.")

        # Statistical association explanation
        sig_names = [t['variable_label'] for t in significant_vars[:3]]
        stat_text = (
            f"Statistical hypothesis testing confirmed statistically significant associations (p < 0.05) "
            f"for variables: {', '.join(sig_names)} with vehicle fault patterns."
        )
        
        # Bayesian synthesis explanation
        bayes_text = (
            f"The pgmpy Bayesian Network integrated all sensor states and observed symptoms as conditional evidence. "
            f"Propagating evidence through learned TabularCPDs yielded a posterior probability of "
            f"{top_prob * 100:.1f}% for {top_fault.replace('_', ' ').title()}."
        )

        return {
            'observational_facts': reasons if reasons else ["All sensor readings within normal operating parameters."],
            'statistical_rationale': stat_text,
            'bayesian_rationale': bayes_text
        }

    def _calculate_evidence_importance(self, inputs, evidence, top_fault):
        """
        Calculates exact quantitative evidence contribution scores for each variable
        towards the diagnosed top fault using leave-one-out Bayesian probability shifts.
        """
        base_probs = query_bayesian_diagnosis(evidence)
        base_top_p = base_probs.get(top_fault, 0.001)
        
        importance_scores = []
        
        for key, val in evidence.items():
            # Leave-one-out query
            reduced_evidence = {k: v for k, v in evidence.items() if k != key}
            new_probs = query_bayesian_diagnosis(reduced_evidence)
            new_top_p = new_probs.get(top_fault, 0.001)
            
            # Absolute shift in probability when this evidence item is included vs excluded
            delta = abs(base_top_p - new_top_p)
            importance_scores.append({
                'variable': key,
                'label': key.replace('_state', '').replace('_', ' ').title(),
                'state': val,
                'raw_score': float(delta)
            })
            
        # Normalize scores to 0 - 100% scale
        total_delta = sum(item['raw_score'] for item in importance_scores)
        if total_delta > 0:
            for item in importance_scores:
                item['importance_percent'] = round((item['raw_score'] / total_delta) * 100, 1)
        else:
            for item in importance_scores:
                item['importance_percent'] = round(100.0 / len(importance_scores), 1)
                
        # Sort by importance descending
        importance_scores.sort(key=lambda x: x['importance_percent'], reverse=True)
        return importance_scores

    def _get_sensor_statuses(self, inputs):
        """
        Evaluates sensor health statuses: NORMAL, WARNING, CRITICAL.
        """
        statuses = {}
        
        # Battery Voltage
        bv = inputs['battery_voltage']
        if bv < 11.5 or bv > 15.2:
            statuses['battery'] = {'state': 'CRITICAL', 'color': '#ef4444', 'message': f'{bv} V (Severe Low/High)'}
        elif bv < 12.4 or bv > 14.8:
            statuses['battery'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{bv} V (Marginal)'}
        else:
            statuses['battery'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{bv} V (Normal)'}
            
        # Alternator Voltage
        av = inputs['alternator_voltage']
        if av < 12.5 or av > 15.5:
            statuses['alternator'] = {'state': 'CRITICAL', 'color': '#ef4444', 'message': f'{av} V (Output Low/Overcharge)'}
        elif av < 13.5:
            statuses['alternator'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{av} V (Low Charging)'}
        else:
            statuses['alternator'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{av} V (Normal Charging)'}
            
        # Engine Temperature
        et = inputs['engine_temperature']
        if et > 108.0:
            statuses['engine_temp'] = {'state': 'CRITICAL', 'color': '#ef4444', 'message': f'{et} °C (Overheating)'}
        elif et > 98.0:
            statuses['engine_temp'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{et} °C (Elevated)'}
        else:
            statuses['engine_temp'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{et} °C (Optimal)'}

        # Coolant Temperature
        ct = inputs['coolant_temperature']
        if ct > 105.0:
            statuses['coolant'] = {'state': 'CRITICAL', 'color': '#ef4444', 'message': f'{ct} °C (Boiling Risk)'}
        elif ct > 95.0:
            statuses['coolant'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{ct} °C (High)'}
        else:
            statuses['coolant'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{ct} °C (Normal)'}

        # Oil Pressure
        op = inputs['oil_pressure']
        if op < 18.0:
            statuses['oil_pressure'] = {'state': 'CRITICAL', 'color': '#ef4444', 'message': f'{op} PSI (Dangerously Low)'}
        elif op < 25.0:
            statuses['oil_pressure'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{op} PSI (Low)'}
        else:
            statuses['oil_pressure'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{op} PSI (Normal)'}

        # Engine RPM
        rpm = inputs['engine_rpm']
        if rpm < 500 or rpm > 4500:
            statuses['rpm'] = {'state': 'WARNING', 'color': '#f59e0b', 'message': f'{rpm} RPM (Abnormal Idle/High)'}
        else:
            statuses['rpm'] = {'state': 'NORMAL', 'color': '#10b981', 'message': f'{rpm} RPM (Stable)'}

        return statuses
