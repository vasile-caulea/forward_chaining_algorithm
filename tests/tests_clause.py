import unittest
from fca_algorithm.literal import Literal
from fca_algorithm.clause import Clause


class TestClause(unittest.TestCase):
    def test_init(self):
        clause_str = "c(Alice) and y(Smith) -> z(Bob)"
        clause = Clause(clause_str)

        self.assertEqual(len(clause.premises), 2)
        self.assertEqual(clause.premises[0], Literal("c(Alice)"))
        self.assertEqual(clause.premises[1], Literal("y(Smith)"))
        self.assertEqual(clause.conclusion, Literal("z(Bob)"))

    def test_create_new(self):
        premises = [Literal("c(Alice)"), Literal("y(Smith)")]
        conclusion = Literal("z(Bob)")
        new_clause = Clause.create_new(premises, conclusion)

        self.assertEqual(new_clause.premises, premises)
        self.assertEqual(new_clause.conclusion, conclusion)

    def test_match(self):
        clause1 = Clause("c(x) and y(m) -> z(x)")
        clause2 = Clause("y(b) and c(a) -> z(a)")
        clause3 = Clause.create_new([Literal("c(a)"), Literal("m(s)")], None)
        self.assertTrue(clause1.match(clause2))
        self.assertFalse(clause1.match(clause3))

    def test_is_rule(self):
        rule_clause = Clause("c(x) -> y(x)")
        non_rule_clause = Clause.create_new([Literal("c(John)"), Literal("y(Doe)")], None)

        self.assertTrue(rule_clause.is_rule())
        self.assertFalse(non_rule_clause.is_rule())

    def test_get_substitution(self):
        clause1 = Clause("c(x) and y(k) -> z(x)")
        clause2 = Clause.create_new([Literal("c(John)"), Literal("y(Doe)")], None)
        substitution = clause1.get_substitution(clause2)
        expected_substitution = Literal("z(John)")
        self.assertEqual(substitution, expected_substitution)

    def test_equality(self):
        clause1 = Clause("c(Alice) and y(Smith) -> z(Bob)")
        clause2 = Clause("c(Alice) and y(Smith) -> z(Bob)")
        clause3 = Clause("a(John) and b(Doe) -> c(Charlie)")

        self.assertEqual(clause1, clause2)
        self.assertNotEqual(clause1, clause3)
