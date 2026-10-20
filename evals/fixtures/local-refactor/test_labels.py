import unittest
from labels import labels

class LabelTests(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(labels([" A ", "", " ", "B", " A "]), ["a", "b", "a"])
