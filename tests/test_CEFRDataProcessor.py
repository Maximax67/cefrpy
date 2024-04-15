import unittest

from math import inf
from cefrpy import CEFRDataProcessor, POSTag

class TestCEFRDataProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_word = "test"
        cls.valid_word_pos_id = int(POSTag.NN)
        cls.valid_word_unknown_pos_id = int(POSTag.CD)
        cls.not_valid_words_test_pos_tag = int(POSTag.CC)
        cls.not_valid_words = ("", "@test@", "notvalidword", "toolongwordtoolongwordtoolongwordtoolongwordtoolongword")
        cls.processor = CEFRDataProcessor()

    def test_get_wlp_and_max_word_len(self):
        self.assertTrue(0 < self.processor.get_max_word_len() < 255)

    def test_word_len_invalid(self):
        min_invalid_word_len = self.processor.get_max_word_len() + 1

        self.assertFalse(self.processor.is_word_len_valid(-inf))
        self.assertFalse(self.processor.is_word_len_valid(-1))
        self.assertFalse(self.processor.is_word_len_valid(0))
        self.assertFalse(self.processor.is_word_len_valid(inf))
        self.assertFalse(self.processor.is_word_len_valid(256))
        self.assertFalse(self.processor.is_word_len_valid(min_invalid_word_len))

    def test_word_len_valid(self):
        max_valid_word_len = self.processor.get_max_word_len()

        self.assertTrue(self.processor.is_word_len_valid(1))
        self.assertTrue(self.processor.is_word_len_valid(max_valid_word_len))

    def test_pack_word(self):
        self.assertEqual(CEFRDataProcessor.pack_word("test"), b'test')

    def test_byte_int_level_to_float(self):
        self.assertAlmostEqual(CEFRDataProcessor.byte_int_level_to_float(0), 1)
        self.assertAlmostEqual(CEFRDataProcessor.byte_int_level_to_float(250), 6)

    def test_byte_int_level_to_float_invalid(self):
        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(-1)

        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(256)

        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(257)

        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(251)

        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(inf)

        with self.assertRaises(ValueError):
            CEFRDataProcessor.byte_int_level_to_float(-inf)

    def test_is_word_in_database(self):
        self.assertTrue(self.processor.is_word_in_database(self.valid_word))

        for word in self.not_valid_words:
            self.assertFalse(self.processor.is_word_in_database(word))

    def test_is_word_pos_in_database(self):
        self.assertTrue(self.processor.is_word_pos_id_database(self.valid_word, self.valid_word_pos_id))
        self.assertFalse(self.processor.is_word_pos_id_database(self.valid_word, self.valid_word_unknown_pos_id))

        for word in self.not_valid_words:
            self.assertFalse(self.processor.is_word_pos_id_database(word, self.not_valid_words_test_pos_tag))

    def test_get_word_level_for_pos_id(self):
        self.assertIsNotNone(self.processor.get_word_level_for_pos_id(self.valid_word, self.valid_word_pos_id, False))
        self.assertIsNone(self.processor.get_word_level_for_pos_id(self.valid_word, inf, False))

        self.assertIsNone(self.processor.get_word_level_for_pos_id(self.valid_word, inf, False))
        self.assertIsNotNone(self.processor.get_word_level_for_pos_id(self.valid_word, inf, True))

        for word in self.not_valid_words:
            self.assertIsNone(self.processor.get_word_level_for_pos_id(word, self.not_valid_words_test_pos_tag, True))
            self.assertIsNone(self.processor.get_word_level_for_pos_id(word, self.not_valid_words_test_pos_tag, False))

    def test_get_word_count_for_length(self):
        self.assertTrue(0 <= self.processor.get_word_count_for_length(1) <= 26)

        valid_word_len = len(self.valid_word)
        self.assertTrue(1 <= self.processor.get_word_count_for_length(valid_word_len) <= pow(26, valid_word_len))

    def test_word_pos_count_for_length(self):
        self.assertGreaterEqual(self.processor.get_word_pos_count_for_length(1), 0)

        valid_word_len = len(self.valid_word)
        self.assertGreater(self.processor.get_word_pos_count_for_length(valid_word_len), 0)


if __name__ == '__main__':
    unittest.main()
