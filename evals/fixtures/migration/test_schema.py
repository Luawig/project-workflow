import sqlite3
import unittest
from schema import create_schema

class SchemaTests(unittest.TestCase):
    def test_existing_data(self):
        con = sqlite3.connect(":memory:")
        create_schema(con)
        con.execute("INSERT INTO items VALUES (1, 'one')")
        con.commit()
        self.assertEqual(con.execute("SELECT * FROM items").fetchall(), [(1, "one")])
        con.close()
