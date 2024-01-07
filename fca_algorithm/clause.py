from fca_algorithm.literal import Literal


class Clause:
    def __init__(self, clause: str):
        if clause:
            premises, conclusion = clause.split('->')
            self.premises: list[Literal] = [Literal(x) for x in premises.split('and')]
            self.conclusion: Literal = Literal(conclusion)

    @classmethod
    def create_new(cls, premises, conclusion) -> 'Clause':
        clause = cls('')
        clause.premises = premises
        clause.conclusion = conclusion
        return clause

    def match(self, clause: 'Clause') -> bool:
        """Checks if the clause has the same premises as the received one"""
        if len(self.premises) != len(clause.premises):
            return False

        premises_set = set([x.name for x in self.premises])
        clause_premises_set = set([x.name for x in clause.premises])
        return premises_set == clause_premises_set

    def is_rule(self) -> bool:
        """Checks if the clause is a rule (has a conclusion)"""
        return self.conclusion is not None

    def get_substitution(self, clause: 'Clause') -> 'Literal' or None:
        """Gets a substitution for the clause rule (self) with the received clause"""
        theta = {}
        for i in range(len(self.premises)):
            if self.premises[i].is_same_type_with(clause.premises[i]):
                substitution = self.premises[i].substitute_with(clause.premises[i])
                if substitution is None:
                    return None
                for key in substitution:
                    # for case {x: 'Jane'} and then {x: 'John'}
                    if key in theta and theta[key] != substitution[key]:
                        return None
                    else:
                        theta[key] = substitution[key]
            else:
                return None
        if len(theta) == 0:
            return None
        literal = Literal('')
        literal.name = self.conclusion.name
        for value in self.conclusion.values:
            if value in theta:
                literal.values.append(theta[value])
            else:
                literal.values.append(value)
        return literal

    def __eq__(self, other: 'Clause'):
        if other is None:
            return False

        if self.conclusion != other.conclusion:
            return False

        if len(self.premises) != len(other.premises):
            return False

        for i in range(len(self.premises)):
            if self.premises[i] != other.premises[i]:
                return False

        return True

    def __repr__(self):
        result = ' AND '.join(map(str, self.premises))
        if self.conclusion:
            result += f' -> {self.conclusion}'
        return result
