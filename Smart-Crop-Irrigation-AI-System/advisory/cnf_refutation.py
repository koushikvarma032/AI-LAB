"""
SymPy-Powered CNF Refutation Theorem Proving Engine.
Performs automated conversion of domain knowledge to Conjunctive Normal Form (CNF)
and carries out step-by-step Propositional Resolution Refutation:
KB |= Q  <===>  KB and ~Q is Unsatisfiable (Derives Empty Clause [] / Contradiction).
"""

import time
from typing import List, Set, Dict, Tuple, Optional, Any
import sympy
from sympy.logic.boolalg import to_cnf, Or, And, Not, Implies
from sympy.logic.inference import satisfiable

from .models import Fact, Rule, ResolutionStep, RefutationProofResult


def sympy_literal_to_str(lit: sympy.Basic) -> str:
    """Pretty prints a SymPy literal."""
    if isinstance(lit, Not):
        return f"~{lit.args[0]}"
    return str(lit)


def clause_to_str(lits: Set[sympy.Basic]) -> str:
    """Formats a set of literals as a readable disjunctive clause."""
    if not lits:
        return "[] (Empty Clause / Contradiction)"
    return " v ".join(sorted([sympy_literal_to_str(l) for l in lits]))


class SymPyCNFRefutationEngine:
    """
    Automated Theorem Prover using SymPy and Propositional Resolution Refutation.
    """
    def __init__(self):
        self._symbols_cache: Dict[str, sympy.Symbol] = {}

    def get_symbol(self, name: str) -> sympy.Symbol:
        clean = name.replace(" ", "_").replace("-", "_").replace("(", "_").replace(")", "")
        if clean not in self._symbols_cache:
            self._symbols_cache[clean] = sympy.symbols(clean)
        return self._symbols_cache[clean]

    def rule_to_sympy(self, rule: Rule, target: str) -> sympy.Basic:
        """
        Converts Rule (A1 ^ A2 -> C) into SymPy Implies expression.
        """
        ant_syms = [self.get_symbol(f"{ant}_{target}") for ant in rule.antecedents]
        cons_sym = self.get_symbol(f"{rule.consequent}_{target}")
        if len(ant_syms) == 1:
            antecedent_expr = ant_syms[0]
        else:
            antecedent_expr = And(*ant_syms)
        return Implies(antecedent_expr, cons_sym)

    def fact_to_sympy(self, fact: Fact) -> sympy.Basic:
        sym = self.get_symbol(f"{fact.predicate}_{fact.target}")
        return sym if fact.value else Not(sym)

    def extract_clauses_from_expr(self, expr: sympy.Basic) -> List[Set[sympy.Basic]]:
        """
        Converts a SymPy Boolean expression into CNF and returns a list of clauses
        (each clause is a set of literal expressions).
        """
        cnf = to_cnf(expr, simplify=True)
        clauses: List[Set[sympy.Basic]] = []
        if isinstance(cnf, And):
            conjuncts = cnf.args
        else:
            conjuncts = [cnf]

        for conj in conjuncts:
            if isinstance(conj, Or):
                lits = set(conj.args)
            else:
                lits = {conj}
            clauses.append(lits)
        return clauses

    def prove(
        self,
        rules: List[Rule],
        facts: List[Fact],
        query_predicate: str,
        target: str
    ) -> RefutationProofResult:
        """
        Proves whether KB |= query_predicate(target) via CNF Resolution Refutation.
        """
        start_time = time.perf_counter()

        # Target symbol and query
        query_sym = self.get_symbol(f"{query_predicate}_{target}")
        query_fol = f"{query_predicate}({target})"
        negated_query = Not(query_sym)

        # Build KB expressions
        rule_exprs = [self.rule_to_sympy(r, target) for r in rules]
        fact_exprs = [self.fact_to_sympy(f) for f in facts]
        all_kb_exprs = rule_exprs + fact_exprs

        # Full sentence under refutation: KB & ~Query
        full_refutation_sentence = And(*all_kb_exprs, negated_query)

        # 1. Verify satisfiability via SymPy SAT solver
        sat_result = satisfiable(full_refutation_sentence)
        is_unsat = (sat_result is False)

        # 2. Extract initial CNF clauses
        clauses_pool: List[Set[sympy.Basic]] = []
        clause_origins: Dict[int, str] = {}
        initial_clauses_info: List[Tuple[str, str]] = []

        cid = 1
        for rule, expr in zip(rules, rule_exprs):
            extracted = self.extract_clauses_from_expr(expr)
            for c in extracted:
                clauses_pool.append(c)
                lbl = f"C{cid}"
                desc = f"{clause_to_str(c)} [Rule {rule.rule_id}: {rule.name}]"
                clause_origins[cid] = lbl
                initial_clauses_info.append((lbl, desc))
                cid += 1

        for fact, expr in zip(facts, fact_exprs):
            extracted = self.extract_clauses_from_expr(expr)
            for c in extracted:
                clauses_pool.append(c)
                lbl = f"C{cid}"
                desc = f"{clause_to_str(c)} [Fact: {fact.to_fol_repr()} ({fact.source})]"
                clause_origins[cid] = lbl
                initial_clauses_info.append((lbl, desc))
                cid += 1

        # Negated query clause
        neg_clauses = self.extract_clauses_from_expr(negated_query)
        neg_clause_lits = neg_clauses[0]
        neg_cid_lbl = f"C{cid}"
        neg_desc = f"{clause_to_str(neg_clause_lits)} [Negated Goal: ~{query_fol}]"
        initial_clauses_info.append((neg_cid_lbl, neg_desc))
        negated_query_clause = (neg_cid_lbl, neg_desc)
        clauses_pool.append(neg_clause_lits)
        cid += 1

        # 3. Step-by-step resolution refutation theorem proving
        # Working memory: index mapped to (clause_set, label)
        indexed_clauses: Dict[int, Tuple[Set[sympy.Basic], str]] = {}
        for idx, (lbl, desc) in enumerate(initial_clauses_info, 1):
            indexed_clauses[idx] = (clauses_pool[idx - 1], lbl)

        resolution_steps: List[ResolutionStep] = []
        contradiction_found = False
        next_id = len(indexed_clauses) + 1
        max_steps = 150

        # Prioritize unit resolution & set-of-support resolution
        seen_clauses = [frozenset(c) for c in clauses_pool]

        step_idx = 1
        done = False

        # Attempt to find resolution steps towards the empty clause
        while not done and step_idx <= max_steps:
            found_pair = False
            clause_ids = list(indexed_clauses.keys())

            # Sort candidate pairs to favor shorter clauses (unit preference)
            candidate_pairs = []
            for i in range(len(clause_ids)):
                for j in range(i + 1, len(clause_ids)):
                    c1_id = clause_ids[i]
                    c2_id = clause_ids[j]
                    len_sum = len(indexed_clauses[c1_id][0]) + len(indexed_clauses[c2_id][0])
                    candidate_pairs.append((len_sum, c1_id, c2_id))

            candidate_pairs.sort(key=lambda x: x[0])

            for _, id1, id2 in candidate_pairs:
                c1_lits, lbl1 = indexed_clauses[id1]
                c2_lits, lbl2 = indexed_clauses[id2]

                # Check for complementary literals
                for lit in c1_lits:
                    comp_lit = Not(lit) if not isinstance(lit, Not) else lit.args[0]
                    if comp_lit in c2_lits:
                        # Compute resolvent
                        resolvent = (c1_lits - {lit}) | (c2_lits - {comp_lit})
                        f_resolvent = frozenset(resolvent)

                        if f_resolvent not in seen_clauses:
                            seen_clauses.append(f_resolvent)
                            res_lbl = f"C{next_id}"
                            is_empty = (len(resolvent) == 0)
                            res_str = clause_to_str(resolvent)

                            step = ResolutionStep(
                                step_num=step_idx,
                                clause1_id=lbl1,
                                clause1_str=clause_to_str(c1_lits),
                                clause2_id=lbl2,
                                clause2_str=clause_to_str(c2_lits),
                                resolved_literal=sympy_literal_to_str(lit),
                                resolvent_id=res_lbl,
                                resolvent_str=res_str,
                                is_contradiction=is_empty
                            )
                            resolution_steps.append(step)
                            indexed_clauses[next_id] = (resolvent, res_lbl)
                            next_id += 1
                            step_idx += 1
                            found_pair = True

                            if is_empty:
                                contradiction_found = True
                                done = True
                            break
                if done or found_pair:
                    break

            if not found_pair:
                # No new resolvents can be produced
                break

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        sympy_status = (
            "Verified Unsatisfiable (Theorem Proved via SymPy SAT)"
            if is_unsat
            else "Satisfiable (Hypothesis not refuted; cannot be proved)"
        )

        return RefutationProofResult(
            query_symbol=str(query_sym),
            query_fol=query_fol,
            is_proved=is_unsat or contradiction_found,
            initial_clauses=initial_clauses_info,
            negated_query_clause=negated_query_clause,
            resolution_steps=resolution_steps,
            satisfiable_under_negation=not is_unsat,
            sympy_verification_status=sympy_status,
            proof_time_ms=round(elapsed_ms, 2)
        )
