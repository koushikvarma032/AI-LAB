import pandas as pd
import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator, MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from config import Config
from services.dataset_service import load_dataset

class AutoSenseBayesianModel:
    """
    Genuine Bayesian Network implementation for AutoSense Nexus using pgmpy.
    Constructs a Directed Acyclic Graph (DAG) representing sensor, symptom, 
    intermediate health states, and fault nodes.
    Fits TabularCPDs from the dataset using Bayesian parameter estimation.
    """
    
    def __init__(self):
        self.model = None
        self.inference_engine = None
        self.discretized_df = None
        self.build_and_fit()

    @staticmethod
    def discretize_sensors(df):
        """
        Discretizes continuous sensor variables into categorical states required for pgmpy TabularCPDs.
        """
        d_df = df.copy()
        
        # Battery Voltage Discretization
        # States: LOW (<12.0), NORMAL (12.0 - 14.5), HIGH (>14.5)
        d_df['battery_voltage_state'] = pd.cut(
            d_df['battery_voltage'],
            bins=[-np.inf, 11.9, 14.6, np.inf],
            labels=['LOW', 'NORMAL', 'HIGH']
        ).astype(str)
        
        # Alternator Voltage Discretization
        # States: LOW (<13.2), NORMAL (13.2 - 15.0), HIGH (>15.0)
        d_df['alternator_voltage_state'] = pd.cut(
            d_df['alternator_voltage'],
            bins=[-np.inf, 13.1, 15.0, np.inf],
            labels=['LOW', 'NORMAL', 'HIGH']
        ).astype(str)
        
        # Engine Temperature Discretization
        # States: NORMAL (<98.0), HIGH (98.0 - 108.0), CRITICAL (>108.0)
        d_df['engine_temp_state'] = pd.cut(
            d_df['engine_temperature'],
            bins=[-np.inf, 97.9, 107.9, np.inf],
            labels=['NORMAL', 'HIGH', 'CRITICAL']
        ).astype(str)
        
        # Coolant Temperature Discretization
        # States: NORMAL (<95.0), HIGH (95.0 - 105.0), CRITICAL (>105.0)
        d_df['coolant_temp_state'] = pd.cut(
            d_df['coolant_temperature'],
            bins=[-np.inf, 94.9, 104.9, np.inf],
            labels=['NORMAL', 'HIGH', 'CRITICAL']
        ).astype(str)
        
        # Oil Pressure Discretization
        # States: LOW (<25.0), NORMAL (25.0 - 65.0), HIGH (>65.0)
        d_df['oil_pressure_state'] = pd.cut(
            d_df['oil_pressure'],
            bins=[-np.inf, 24.9, 65.0, np.inf],
            labels=['LOW', 'NORMAL', 'HIGH']
        ).astype(str)
        
        # Engine RPM Discretization
        # States: STALL_LOW (<650), NORMAL (650 - 3500), HIGH (>3500)
        d_df['rpm_state'] = pd.cut(
            d_df['engine_rpm'],
            bins=[-np.inf, 649, 3500, np.inf],
            labels=['STALL_LOW', 'NORMAL', 'HIGH']
        ).astype(str)
        
        # Ensure binary symptoms are strings
        for sym in Config.SYMPTOMS:
            d_df[sym] = d_df[sym].astype(str)
            
        return d_df

    def build_and_fit(self):
        """
        Defines the DAG network topology and fits CPDs using dataset.
        """
        raw_df = load_dataset()
        self.discretized_df = self.discretize_sensors(raw_df)
        
        # Define Directed Acyclic Graph (DAG) Edges
        # Fault -> Sensors and Symptoms (Generative Bayesian Diagnostic DAG)
        edges = [
            # Fault to sensor states
            ('fault', 'battery_voltage_state'),
            ('fault', 'alternator_voltage_state'),
            ('fault', 'engine_temp_state'),
            ('fault', 'coolant_temp_state'),
            ('fault', 'oil_pressure_state'),
            ('fault', 'rpm_state'),
            
            # Fault to symptoms
            ('fault', 'slow_cranking'),
            ('fault', 'hard_starting'),
            ('fault', 'dim_headlights'),
            ('fault', 'engine_noise'),
            ('fault', 'overheating_indicator'),
            
            # Symptom inter-dependencies / Intermediate state coupling
            ('battery_voltage_state', 'slow_cranking'),
            ('battery_voltage_state', 'dim_headlights'),
            ('coolant_temp_state', 'overheating_indicator'),
            ('oil_pressure_state', 'engine_noise')
        ]
        
        # Build pgmpy DiscreteBayesianNetwork
        self.model = DiscreteBayesianNetwork(edges)
        
        # Fit CPDs using BayesianEstimator with Dirichlet prior (Laplace smoothing)
        estimator = BayesianEstimator(self.model, self.discretized_df)
        cpds = estimator.get_parameters(prior_type="BDeu", equivalent_sample_size=10)
        
        for cpd in cpds:
            self.model.add_cpds(cpd)
            
        # Verify model consistency
        if not self.model.check_model():
            print("Warning: Bayesian Network model check failed! Double check CPDs.")
            
        # Initialize Variable Elimination inference engine
        self.inference_engine = VariableElimination(self.model)

    def query(self, evidence):
        """
        Calculates posterior probability distribution over 'fault' node given evidence dictionary.
        """
        if self.inference_engine is None:
            self.build_and_fit()
            
        # Clean evidence to ensure only valid network nodes are included
        valid_nodes = set(self.model.nodes())
        filtered_evidence = {k: str(v) for k, v in evidence.items() if k in valid_nodes and v is not None}
        
        try:
            result = self.inference_engine.query(
                variables=['fault'],
                evidence=filtered_evidence,
                joint=False
            )
            fault_cpd = result['fault']
            
            probabilities = {}
            for state, prob in zip(fault_cpd.state_names['fault'], fault_cpd.values):
                probabilities[state] = float(prob)
                
            # Sort by highest probability descending
            sorted_probs = dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))
            return sorted_probs
            
        except Exception as e:
            print(f"Error during Bayesian inference query: {e}")
            # Fallback uniform / prior distribution if query fails
            priors = self.discretized_df['fault'].value_counts(normalize=True).to_dict()
            return priors

    def get_network_structure(self):
        """
        Returns nodes, edges, and node metadata for graph visualizer (Vis.js / React Flow format).
        """
        nodes = []
        for node in self.model.nodes():
            node_type = "fault" if node == "fault" else ("sensor" if "state" in node else "symptom")
            states = list(self.discretized_df[node].unique()) if node in self.discretized_df else []
            nodes.append({
                'id': node,
                'label': node.replace('_', ' ').title(),
                'type': node_type,
                'states': states
            })
            
        edges = []
        for source, target in self.model.edges():
            edges.append({
                'from': source,
                'to': target
            })
            
        return {
            'nodes': nodes,
            'edges': edges
        }
