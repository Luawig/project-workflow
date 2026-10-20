import unittest
from tasks import visible_tasks

class TaskTests(unittest.TestCase):
    def test_order_and_input(self):
        items = [{"id": 2, "title": "b"}, {"id": 1, "title": "a"}]
        self.assertEqual(visible_tasks(items), items)
        self.assertIsNot(visible_tasks(items)[0], items[0])
