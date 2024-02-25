#!/usr/bin/env python

import unittest
import duckdb

from sql_split import process_sql

class TestProcessSQLWithDuckDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Establish a connection to an in-memory DuckDB database
        cls.conn = duckdb.connect(database=':memory:', read_only=False)

    @classmethod
    def tearDownClass(cls):
        # Close the DuckDB connection after all tests are done
        cls.conn.close()

    def test_simple_sql_execution(self):
        input_string = "```sql\nSELECT 1 AS a\n```"
        expected_output = (
            "```sql\nSELECT 1 AS a\n```\n```\n"
            "┌───────┐\n"
            "│   a   │\n"
            "│ int32 │\n"
            "├───────┤\n"
            "│     1 │\n"
            "└───────┘\n"
            "```"
        )
        result = process_sql(self.conn, input_string)
        self.assertEqual(result.strip(), expected_output.strip())

    def test_error_handling(self):
        input_string = "```sql\nSELEC 1 AS a\n```"  # Intentional typo in SELECT
        expected_output = "```sql\nSELEC 1 AS a\n```\n```\nSQL Execution Error: Parser Error: syntax error at or near \"SELEC\"\n```\n"
        result = process_sql(self.conn, input_string)
        self.assertEqual(result, expected_output)

    def test_mixed_content(self):
        input_string = "Some text.\n```sql\nSELECT 2 AS b\n```"
        expected_output = (
            "Some text.\n```sql\nSELECT 2 AS b\n```\n```\n"
            "┌───────┐\n"
            "│   b   │\n"
            "│ int32 │\n"
            "├───────┤\n"
            "│     2 │\n"
            "└───────┘\n"
            "```"
        )
        result = process_sql(self.conn, input_string)
        self.assertEqual(result.strip(), expected_output.strip())

    def test_empty_input(self):
        input_string = ""
        expected_output = "\n"
        result = process_sql(self.conn, input_string)
        self.assertEqual(result, expected_output)

    def test_text_sql_text_content(self):
        input_string = (
            "This is introductory text.\n"
            "```sql\nSELECT 3 AS c\n```\n"
            "This is concluding text."
        )
        expected_output = (
            "This is introductory text.\n"
            "```sql\nSELECT 3 AS c\n```\n"
            "```\n"
            "┌───────┐\n"
            "│   c   │\n"
            "│ int32 │\n"
            "├───────┤\n"
            "│     3 │\n"
            "└───────┘\n"
            "```\n"
            "This is concluding text.\n"
        )
        result = process_sql(self.conn, input_string)
        self.assertEqual(result.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
