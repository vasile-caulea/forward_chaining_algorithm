class Literal:
    def __init__(self, literal: str):
        self.values = []
        self.name = None
        if literal:
            vals = literal.replace(' ', '').split('(')
            self.name = vals[0]
            self.values = vals[1].replace(')', '').split(',')

    def is_same_type_with(self, literal: 'Literal') -> bool:
        """Checks if the literal is the same type as the received one (have the same name)"""
        return self.name == literal.name

    def substitute_with(self, other: 'Literal') -> dict[str, str]:
        """Determines a substitution for the values with the received literal"""
        result = {}
        for i in range(0, len(self.values)):
            if self.values[i] != other.values[i]:
                result[self.values[i]] = other.values[i]
        return result

    def __eq__(self, other: 'Literal') -> bool:
        if other is None:
            return False
        if self.name != other.name:
            return False

        for i in range(0, len(self.values)):
            if self.values[i] != other.values[i]:
                return False
        return True

    def __repr__(self):
        return f'{self.name}({", ".join(self.values)})'
