import unittest

from fca_algorithm.kb import KnowledgeBase


class TestKnowledgeBase(unittest.TestCase):

    def setUp(self):
        self.valid_lines = [
            "kb:",
            "c(x) and y(k) -> z(x)",
            "y(Smith)",
            "c(Alice)",
            "query:",
            "z(Bob)"
        ]
        self.invalid_lines = [
            "kb:",
            "invalid_clause",
            "query:",
            "z(Bob)"
        ]

    def test_init_valid_lines(self):
        kb = KnowledgeBase(self.valid_lines)
        self.assertEqual(len(kb.get_rule_clauses()), 1)
        self.assertEqual(len(kb.get_theta(kb.get_rule_clauses()[0])), 2)

    def test_init_invalid_lines(self):
        with self.assertRaises(Exception):
            kb = KnowledgeBase(self.invalid_lines)


if __name__ == '__main__':
    unittest.main()
