from fca_algorithm.clause import Clause
from fca_algorithm.kb import KnowledgeBase
from fca_algorithm.literal import Literal


def demonstrate(knb: KnowledgeBase):
    steps = []
    iteration = 1
    while True:
        print(f'Iteration {iteration}'.center(50, '-'))
        new = []
        for rule_clause in knb.get_rule_clauses():
            for theta in knb.get_theta(rule_clause):
                conclusion = rule_clause.get_substitution(theta)
                if conclusion and (not knb.contains_clause(conclusion)) and (conclusion not in new):
                    print(f'{theta} -> {conclusion}')
                    new.append(conclusion)
                    steps.append((theta, conclusion))
                    if knb.is_solution(conclusion):
                        return True, steps
        knb.add_new_clauses(new)
        if len(new) == 0:
            break
        iteration += 1
    return False, steps


def get_solution(demonstration_steps: list[tuple[Clause, Literal]]) -> list[tuple[Clause, Literal]]:
    last_step = demonstration_steps[-1]
    i = 0
    while i < len(demonstration_steps):
        elem = demonstration_steps[i]
        found = False
        for elem2 in demonstration_steps:
            if elem[1] in elem2[0].premises:
                found = True
                break
        if not found:
            demonstration_steps.remove(elem)
        else:
            i += 1
    demonstration_steps.append(last_step)
    return demonstration_steps
