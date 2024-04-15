import unittest

from math import inf
from cefrpy import POSTag

class TestPOSTag(unittest.TestCase):
    def setUp(self):
        self.total_tags = POSTag.get_total_tags()

    def test_total_tags_count(self):
        self.assertEqual(len(POSTag.__members__), self.total_tags)

    def test_tag_id_and_name(self):
        for i in range(self.total_tags):
            tag = POSTag(i)
            tag_name = str(tag)
            tag_id = int(tag)

            self.assertEqual(tag_id, i)
            self.assertEqual(tag_name, POSTag(i).name)

    def test_tag_description(self):
        for i in range(self.total_tags):
            tag = POSTag(i)
            tag_desctiption = tag.get_description()
            description_by_tag_id = POSTag.get_description_by_tag_id(i)
            tag_name = str(tag)
            description_by_tag_name = POSTag.get_description_by_tag_name(tag_name)

            self.assertEqual(description_by_tag_id, tag_desctiption)
            self.assertEqual(description_by_tag_name, tag_desctiption)

    def test_tag_from_name(self):
        for i in range(self.total_tags):
            tag = POSTag(i)
            tag_name = str(tag)
            tag_from_name = POSTag.from_tag_name(tag_name)

            self.assertTrue(tag_from_name == tag)

    def test_different_tags_comparison(self):
        for i in range(self.total_tags):
            tag = POSTag(i)
            other_tag_id = i - 1 if i != 0 else self.total_tags - 1
            other_tag = POSTag(other_tag_id)

            self.assertFalse(other_tag == tag)

    def test_invalid_pos_tags_operations(self):
        invalid_tag_values = ("", "INVALID", "&^%@**@!$()")

        with self.assertRaises(ValueError):
            POSTag(inf)

        with self.assertRaises(ValueError):
            POSTag(-inf)

        with self.assertRaises(ValueError):
            POSTag(-1)

        with self.assertRaises(ValueError):
            POSTag(self.total_tags)

        for invalid_tag_value in invalid_tag_values:
            with self.assertRaises(ValueError):
                POSTag.from_tag_name(invalid_tag_value)

            with self.assertRaises(ValueError):
                POSTag.get_id_by_tag_name(invalid_tag_value)

            with self.assertRaises(ValueError):
                POSTag.get_description_by_tag_name(invalid_tag_value)

    def test_get_all_tags(self):
        pos_tags = POSTag.get_all_tags()

        self.assertIsInstance(pos_tags, list)
        self.assertEqual(len(pos_tags), self.total_tags)

        for pos_tag in pos_tags:
            self.assertIsNotNone(POSTag.get_id_by_tag_name(pos_tag))
            self.assertIsNotNone(POSTag.get_description_by_tag_name(pos_tag))
            self.assertIsNotNone(POSTag.__members__.get(pos_tag))


if __name__ == '__main__':
    unittest.main()
