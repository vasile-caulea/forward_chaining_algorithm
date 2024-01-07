from fca_algorithm.clause import Clause
from fca_algorithm.kb import KnowledgeBase
from fca_algorithm.literal import Literal


def demonstrate(knb: KnowledgeBase):
    steps = []
    while True:
        new = []
        for rule_clause in knb.get_rule_clauses():
            for theta in knb.get_theta(rule_clause):
                conclusion = rule_clause.get_substitution(theta)
                print(f'{theta} -> {conclusion}')
                if conclusion and (not knb.contains_clause(conclusion)) and (conclusion not in new):
                    new.append(conclusion)
                    steps.append((theta, conclusion))
                    if knb.is_solution(conclusion):
                        return True, steps
        knb.add_new_clauses(new)
        if len(new) == 0:
            break
    return False, steps


def get_solution(demonstration_steps: list[tuple[Clause, Literal]]) -> list[tuple[Clause, Literal]]:
    last_step = demonstration_steps[-1]
    for elem in demonstration_steps:
        if elem[1] not in last_step[0].premises and id(elem[0]) != id(last_step[0]):
            demonstration_steps.remove(elem)
    return demonstration_steps
