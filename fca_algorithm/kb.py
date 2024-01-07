import itertools
import re

from fca_algorithm.clause import Clause
from fca_algorithm.literal import Literal

KB_IDENTIFIER = 'kb:'
QUERY_IDENTIFIER = 'query:'
keywords = ['and', 'query', 'kb']
keywords_pattern = re.compile('|'.join(keywords), flags=re.IGNORECASE)


class KnowledgeBase:
    def __init__(self, lines: list[str]):
        self.__rule_clauses: list[Clause] = []
        self.__fact_clauses: list[Literal] = []
        self.__query: Literal

        lines = filter(lambda x: x != '', map(str.strip, lines))

        try:
            lines = [keywords_pattern.sub(lambda x: x.group(0).lower(), x) for x in lines]
            kb_start_index = lines.index(KB_IDENTIFIER)
            query_start_index = lines.index(QUERY_IDENTIFIER)
            if query_start_index < kb_start_index:
                kb_end_index = len(lines)
            else:
                kb_end_index = query_start_index

            for line in lines[kb_start_index + 1:kb_end_index]:
                if '->' in line:
                    self.__rule_clauses.append(Clause(line))
                else:
                    self.__fact_clauses.append(Literal(line))

            self.__query = Literal(lines[query_start_index + 1])
        except Exception:
            raise Exception(f'Invalid file format')

    def get_rule_clauses(self) -> list[Clause]:
        """Returns all the clauses that are rules (have a conclusion)"""
        return self.__rule_clauses

    def is_solution(self, clause: Literal) -> bool:
        """Checks if the received clause is the solution"""
        return clause == self.__query

    def add_new_clauses(self, new: list[Literal]) -> None:
        """Adds new clauses to the facts knowlede base"""
        self.__fact_clauses.extend(new)

    def contains_clause(self, conclusion: Literal) -> bool:
        """Checks if clause exists in the facts knowledge base"""
        return conclusion in self.__fact_clauses

    def get_theta(self, clause_rule: Clause) -> list[Clause]:
        """Gets all the possible substitutions for the clause rule"""
        possible_substitutions = list()
        for literal in clause_rule.premises:
            for clause in self.__fact_clauses:
                if literal.is_same_type_with(clause) and clause not in possible_substitutions:
                    possible_substitutions.append(clause)

        print("---------------------------")
        print(possible_substitutions)
        print(clause_rule.premises)

        # for each possible substitution, create a combination of premises that match the premises of the rule clause
        substitutions = []
        values = itertools.product(possible_substitutions, repeat=len(clause_rule.premises))

        for premises in values:
            clause = Clause.create_new(premises, None)
            if clause.match(clause_rule):
                substitutions.append(clause)
        print(substitutions)
        print("---------------------------")
        return substitutions

    def __repr__(self):
        result = 'Rules:\n'
        result += '\n'.join(map(str, self.__rule_clauses))
        result += '\n\nFacts:\n'
        result += '\n'.join(map(str, self.__fact_clauses))
        result += f'\n\nQuery: {self.__query}'
        return result

    def get_rules_as_string(self):
        return '\n'.join(map(str, self.__rule_clauses))

    def get_facts_as_string(self):
        return '\n'.join(map(str, self.__fact_clauses))

    def get_query_as_string(self):
        return str(self.__query)
