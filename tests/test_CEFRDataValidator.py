import unittest

from math import inf
from cefrpy import CEFRDataValidator


class TestCEFRDataValidation(unittest.TestCase):
    def setUp(self):
        self.valid_wlp_lengths = [2, 3, 100, 254, 255]
        self.invalid_wlp_lengths = [-inf, -1, 0, 1, 256, 500, inf]

        self.valid_wlp_arrays = [
            [0, 9],
            [0, 6, 10],
            [3, 6, 6, 6, 12]
        ]

        self.invalid_wlp_arrays = [
            [],
            [0],
            [0, -1],
            [1, 2, 3, 4, 5],
            [0, 3, 5, 12],
            [3, 12, 9, 12, 17]
        ]

        self.valid_data = [
            bytearray(b'a\x00\x00d\x03\x05z\x02\x10'),
            bytearray(b'g\x10\x05y\x04\x89kk\x05\x12'),
            bytearray(b'---c\x06\x15qwer\x10\x35----')
        ]

        self.invalid_data = [
            bytearray(b'something\x00\x02test\x00\x01'),
            bytearray(b'hello'),
            bytearray(b'c\x06qwer\x10\x35'),
            bytearray(b'a\x99\x99d\x03\x05z\x02\x10'),
            bytearray(b'testsomething'),
            bytearray(b'#\x00\x00@\x03\x05#\x02\x10')
        ]

    def test_wlp_length_valid(self):
        for length in self.valid_wlp_lengths:
            self.assertTrue(CEFRDataValidator.is_wlp_length_valid(length))

    def test_wlp_length_invalid(self):
        for length in self.invalid_wlp_lengths:
            self.assertFalse(CEFRDataValidator.is_wlp_length_valid(length))

    def test_wlp_array_valid(self):
        for array in self.valid_wlp_arrays:
            self.assertTrue(CEFRDataValidator.is_wlp_array_valid(array))

    def test_wlp_array_invalid(self):
        for array in self.invalid_wlp_arrays:
            self.assertFalse(CEFRDataValidator.is_wlp_array_valid(array))

    def test_cefr_data_valid(self):
        for wlp_array, data in zip(self.valid_wlp_arrays, self.valid_data):
            self.assertTrue(CEFRDataValidator.is_data_valid(wlp_array, data))

    def test_cefr_data_invalid(self):
        for wlp_array, data in zip(self.valid_wlp_arrays, self.invalid_data):
            self.assertFalse(CEFRDataValidator.is_data_valid(wlp_array, data))

        for wlp_array, data in zip(self.invalid_wlp_arrays, self.valid_data):
            self.assertFalse(CEFRDataValidator.is_data_valid(wlp_array, data))


if __name__ == '__main__':
    unittest.main()
