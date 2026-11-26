"""
Auditable Modus Ponens Forward Chaining Inference Engine.
Enforces classical deductive reasoning:
Given Premise alpha and Implication (alpha -> beta), infer beta.
Records an immutable, auditable log of every inference step.
"""

from typing import List, Set, Dict, Optional, Tuple
from datetime import datetime
from .models import Fact, Rule, DeductionStep
from .knowledge_base import AgriculturalKnowledgeBase


class ModusPonensDeductionEngine:
    """
    Executes forward chaining deduction over First-Order ground propositions
    using strict Modus Ponens:
         P, P -> Q
         ---------
             Q
    """
    def __init__(self, knowledge_base: AgriculturalKnowledgeBase):
        self.kb = knowledge_base
        self.audit_trail: List[DeductionStep] = []

    def infer(self, initial_facts: List[Fact], target: str) -> Tuple[List[Fact], List[DeductionStep]]:
        """
        Runs exhaustive forward chaining until closure, maintaining a complete audit trail.
        """
        known_facts: Dict[str, Fact] = {}
        for f in initial_facts:
            known_facts[f.predicate] = f

        fired_rules: Set[str] = set()
        deduction_steps: List[DeductionStep] = []
        step_counter = 1

        while True:
            new_rule_fired = False

            for rule in self.kb.rules:
                if rule.rule_id in fired_rules:
                    continue

                # Check if all antecedents are present in known_facts and True
                antecedents_satisfied = True
                matched_premises: List[Fact] = []

                for ant in rule.antecedents:
                    if ant in known_facts and known_facts[ant].value is True:
                        matched_premises.append(known_facts[ant])
                    else:
                        antecedents_satisfied = False
                        break

                if antecedents_satisfied:
                    # Consequent to deduce
                    consequent_pred = rule.consequent

                    # Construct new deduced fact
                    deduced_fact = Fact(
                        predicate=consequent_pred,
                        target=target,
                        value=True,
                        source=f"Modus Ponens deduction via Rule [{rule.rule_id}] at Step #{step_counter}",
                        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )

                    # Formal Modus Ponens schema notation
                    ant_repr = " ^ ".join([p.to_fol_repr() for p in matched_premises])
                    implication_repr = f"({ant_repr}) -> {deduced_fact.to_fol_repr()}"
                    formal_mp = (
                        f"Premise(s): {ant_repr}\n"
                        f"Rule [{rule.rule_id}]: {implication_repr}\n"
                        f"Deduction:   [Modus Ponens] |- {deduced_fact.to_fol_repr()}"
                    )

                    step = DeductionStep(
                        step_num=step_counter,
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        premises=matched_premises,
                        consequent=deduced_fact,
                        formal_modus_ponens=formal_mp,
                        rationale=rule.agronomic_rationale,
                        timestamp=deduced_fact.timestamp
                    )

                    deduction_steps.append(step)
                    known_facts[consequent_pred] = deduced_fact
                    fired_rules.add(rule.rule_id)
                    step_counter += 1
                    new_rule_fired = True
                    break  # Continue loop with updated facts

            if not new_rule_fired:
                break

        self.audit_trail = deduction_steps
        return list(known_facts.values()), deduction_steps


# Type annotation helper
from typing import Tuple
