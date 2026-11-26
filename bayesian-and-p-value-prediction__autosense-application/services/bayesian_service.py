from models.bayesian_network import AutoSenseBayesianModel

_model_instance = None

def get_bayesian_model():
    """
    Returns singleton instance of AutoSenseBayesianModel.
    """
    global _model_instance
    if _model_instance is None:
        _model_instance = AutoSenseBayesianModel()
    return _model_instance

def query_bayesian_diagnosis(evidence):
    """
    Queries Bayesian Network for posterior fault probabilities given evidence.
    Returns sorted dictionary {fault: posterior_probability}.
    """
    model = get_bayesian_model()
    return model.query(evidence)

def get_bayesian_graph_data():
    """
    Returns DAG structure (nodes, edges, node metadata) for graph visualizer.
    """
    model = get_bayesian_model()
    return model.get_network_structure()

def get_node_cpd_tables(node_name):
    """
    Returns Conditional Probability Table (CPD) for a specified node.
    """
    model = get_bayesian_model()
    if node_name in model.model.nodes():
        cpd = model.model.get_cpds(node_name)
        return {
            'variable': cpd.variable,
            'variable_card': cpd.variable_card,
            'values': cpd.values.tolist(),
            'state_names': cpd.state_names
        }
    return None
