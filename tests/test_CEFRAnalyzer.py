import unittest

from random import randint
from cefrpy import CEFRAnalyzer, CEFRDataReader, POSTag, CEFRLevel


class TestCEFRAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_word = "test"
        cls.valid_word_pos = POSTag.NN
        cls.valid_word_unknown_pos = POSTag.CD
        cls.not_valid_words_test_pos_tag = POSTag.CC
        cls.not_valid_words = ("", "@test@", "notvalidword", "toolongwordtoolongwordtoolongwordtoolongwordtoolongword")
        cls.analyzer = CEFRAnalyzer()

    def test_get_max_word_len(self):
        self.assertTrue(0 < self.analyzer.get_max_word_len() < 255)

    def test_get_pos_tag_id(self):
        tag_id = randint(0, POSTag.get_total_tags() - 1)
        tag = POSTag(tag_id)
        tag_str = str(tag)

        self.assertEqual(CEFRAnalyzer.get_pos_tag_id(tag), tag_id)
        self.assertEqual(CEFRAnalyzer.get_pos_tag_id(tag_str), tag_id)

    def test_get_word_pos_level_float(self):
        valid_word_pos_level = self.analyzer.get_word_pos_level_float(self.valid_word, self.valid_word_pos, False)
        valid_avg_word_pos_level = self.analyzer.get_word_pos_level_float(self.valid_word, self.valid_word_unknown_pos, True)
        none_level = self.analyzer.get_word_pos_level_float(self.valid_word, self.valid_word_unknown_pos, False)

        self.assertIsNotNone(valid_word_pos_level)
        self.assertIsNotNone(valid_avg_word_pos_level)
        self.assertIsNone(none_level)

        for word in self.not_valid_words:
            self.assertIsNone(self.analyzer.get_word_pos_level_float(word, self.not_valid_words_test_pos_tag, False))
            self.assertIsNone(self.analyzer.get_word_pos_level_float(word, self.not_valid_words_test_pos_tag, True))

    def test_get_word_pos_level_CEFR(self):
        valid_word_pos_level = self.analyzer.get_word_pos_level_CEFR(self.valid_word, self.valid_word_pos, False)
        valid_avg_word_pos_level = self.analyzer.get_word_pos_level_CEFR(self.valid_word, self.valid_word_unknown_pos, True)
        none_level = self.analyzer.get_word_pos_level_CEFR(self.valid_word, self.valid_word_unknown_pos, False)

        self.assertIsInstance(valid_word_pos_level, CEFRLevel)
        self.assertIsInstance(valid_avg_word_pos_level, CEFRLevel)
        self.assertIsNone(none_level)

        for word in self.not_valid_words:
            self.assertIsNone(self.analyzer.get_word_pos_level_float(word, self.not_valid_words_test_pos_tag, False))
            self.assertIsNone(self.analyzer.get_word_pos_level_float(word, self.not_valid_words_test_pos_tag, True))

    def test_get_avg_word_level_float(self):
        valid_word_level = self.analyzer.get_average_word_level_float(self.valid_word)
        self.assertIsNotNone(valid_word_level)

        for word in self.not_valid_words:
            self.assertIsNone(self.analyzer.get_average_word_level_float(word))

    def test_get_avg_word_level_CEFR(self):
        valid_word_level = self.analyzer.get_average_word_level_CEFR(self.valid_word)
        self.assertIsInstance(valid_word_level, CEFRLevel)

        for word in self.not_valid_words:
            self.assertIsNone(self.analyzer.get_average_word_level_CEFR(word))

    def test_is_word_in_database(self):
        self.assertTrue(self.analyzer.is_word_in_database(self.valid_word))

        for word in self.not_valid_words:
            self.assertFalse(self.analyzer.is_word_in_database(word))

    def test_is_word_pos_in_database(self):
        self.assertTrue(self.analyzer.is_word_pos_id_database(self.valid_word, self.valid_word_pos))
        self.assertFalse(self.analyzer.is_word_pos_id_database(self.valid_word, self.valid_word_unknown_pos))

        for word in self.not_valid_words:
            self.assertFalse(self.analyzer.is_word_pos_id_database(word, self.not_valid_words_test_pos_tag))

    def test_yields(self):
        valid_word_len = len(self.valid_word)
        valid_words = []
        last_word = ""

        total_words = self.analyzer.get_word_count_for_length(valid_word_len)
        total_word_pos = self.analyzer.get_word_pos_count_for_length(valid_word_len)

        for word in self.analyzer.yield_words_with_length(valid_word_len):
            self.assertGreater(word, last_word)
            valid_words.append(word)
            last_word = word

        self.assertEqual(len(valid_words), total_words)

        valid_words_iter = reversed(valid_words)
        for word in self.analyzer.yield_words_with_length(valid_word_len, reverse_order=True):
            self.assertEqual(next(valid_words_iter), word)

        with self.assertRaises(StopIteration):
            next(valid_words_iter)

        valid_words_iter = iter(valid_words)
        word = next(valid_words_iter)
        word_pos_counter = 0

        for data1, data2 in zip(self.analyzer.yield_word_pos_with_length(valid_word_len, pos_tag_as_string=False),
                                self.analyzer.yield_word_pos_level_with_length(valid_word_len, pos_tag_as_string=True)):
            word1, pos1 = data1
            word2, pos2, level = data2

            self.assertEqual(word1, word2)
            self.assertEqual(pos1, POSTag.from_tag_name(pos2))
            self.assertTrue(CEFRLevel.A1 <= level <= CEFRLevel.C2)

            if word != word1:
                while word < word1:
                    word = next(valid_words_iter)

                self.assertEqual(word, word1)

            word_pos_counter += 1

        with self.assertRaises(StopIteration):
            next(valid_words_iter)

        self.assertEqual(word_pos_counter, total_word_pos)

        valid_words_iter = reversed(valid_words)
        word = next(valid_words_iter)
        word_pos_counter = 0

        for data1, data2 in zip(self.analyzer.yield_word_pos_with_length(valid_word_len, pos_tag_as_string=True, reverse_order=True),
                                self.analyzer.yield_word_pos_level_with_length(valid_word_len, pos_tag_as_string=False, word_level_as_float=True, reverse_order=True)):
            word1, pos1 = data1
            word2, pos2, level = data2

            self.assertEqual(word1, word2)
            self.assertEqual(POSTag.from_tag_name(pos1), pos2)
            self.assertTrue(1.0 <= level <= 6.0)

            if word != word1:
                while word > word1:
                    word = next(valid_words_iter)

                self.assertEqual(word, word1)

            word_pos_counter += 1

        with self.assertRaises(StopIteration):
            next(valid_words_iter)

        self.assertEqual(word_pos_counter, total_word_pos)

    def test_yields_alphabetical(self):
        total_words = self.analyzer.get_total_words()
        self.assertGreater(total_words, 0)

        word_counter = 0
        last_word = ""

        for word in self.analyzer.yield_words(reverse_order=False, word_length_sort=False):
            self.assertGreater(word, last_word)
            last_word = word
            word_counter += 1

        self.assertEqual(word_counter, total_words)

        word_counter = 1
        generator = self.analyzer.yield_words(reverse_order=True, word_length_sort=False)
        last_word = next(generator)

        for word in generator:
            self.assertLess(word, last_word)
            last_word = word
            word_counter += 1

        self.assertEqual(word_counter, total_words)

    def test_yields_word_length_sort(self):
        total_words = self.analyzer.get_total_words()
        self.assertGreater(total_words, 0)

        word_counter = 0
        last_len = 0
        last_word = ""

        for word in self.analyzer.yield_words(reverse_order=False, word_length_sort=True):
            word_len = len(word)
            self.assertGreaterEqual(word_len, last_len)

            if word_len == last_len:
                self.assertGreater(word, last_word)
            else:
                last_len = word_len

            last_word = word
            word_counter += 1

        self.assertEqual(word_counter, total_words)

        word_counter = 1
        generator = self.analyzer.yield_words(reverse_order=True, word_length_sort=True)
        last_word = next(generator)
        last_len = len(last_word)

        for word in generator:
            word_len = len(word)
            self.assertLessEqual(word_len, last_len)

            if word_len == last_len:
                self.assertLess(word, last_word)
            else:
                last_len = word_len

            last_word = word
            word_counter += 1

        self.assertEqual(word_counter, total_words)


if __name__ == '__main__':
    unittest.main()
