import unittest

from cefrpy import CEFRLevel

class TestCEFRLevel(unittest.TestCase):
    def setUp(self):
        self.levels = [CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.B1, CEFRLevel.B2, CEFRLevel.C1, CEFRLevel.C2]

    def test_equality(self):
        for level in self.levels:
            self.assertEqual(level, level)

    def test_inequality(self):
        for i, level1 in enumerate(self.levels):
            for j, level2 in enumerate(self.levels):
                if i != j:
                    self.assertNotEqual(level1, level2)

    def test_less_than(self):
        for i, level1 in enumerate(self.levels):
            for j, level2 in enumerate(self.levels):
                if i < j:
                    self.assertLess(level1, level2)

    def test_less_than_or_equal(self):
        for i, level1 in enumerate(self.levels):
            for j, level2 in enumerate(self.levels):
                if i <= j:
                    self.assertLessEqual(level1, level2)

    def test_greater_than(self):
        for i, level1 in enumerate(self.levels):
            for j, level2 in enumerate(self.levels):
                if i > j:
                    self.assertGreater(level1, level2)

    def test_greater_than_or_equal(self):
        for i, level1 in enumerate(self.levels):
            for j, level2 in enumerate(self.levels):
                if i >= j:
                    self.assertGreaterEqual(level1, level2)

    def test_from_string_method(self):
        for level in self.levels:
            str_level = str(level)
            level_from_str = CEFRLevel.from_str(str_level)

            self.assertEqual(level_from_str, level)


if __name__ == '__main__':
    unittest.main()
