"""Tests for html_summary_report.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from html_summary_report import (
    build_html, column_total, is_number, numeric_columns, read_csv,
)

HEADER = ["name", "visits", "sales"]
ROWS = [["Alpha", "120", "15"],
        ["Beta", "80", "9"],
        ["Gamma", "200", "22"]]


class TestHTMLSummaryReport(unittest.TestCase):
    def test_is_number(self):
        self.assertTrue(is_number("42"))
        self.assertTrue(is_number("3.14"))
        self.assertTrue(is_number("1,000"))
        self.assertFalse(is_number("abc"))
        self.assertFalse(is_number(""))
        self.assertFalse(is_number("12x"))

    def test_numeric_columns(self):
        self.assertEqual(numeric_columns(HEADER, ROWS), [1, 2])

    def test_numeric_columns_with_text_mixed_in(self):
        rows = [["a", "10"], ["b", "n/a"]]
        self.assertEqual(numeric_columns(["x", "y"], rows), [])

    def test_column_total(self):
        self.assertEqual(column_total(ROWS, 1), 400)
        self.assertEqual(column_total(ROWS, 2), 46)

    def test_column_total_floats(self):
        rows = [["a", "1.5"], ["b", "2.25"]]
        self.assertEqual(column_total(rows, 1), 3.75)

    def test_build_html_has_table_and_totals(self):
        page = build_html(HEADER, ROWS, title="Test Report")
        self.assertIn("<table>", page)
        self.assertIn("Test Report", page)
        self.assertIn("<td>400</td>", page)   # visits total
        self.assertIn("<td>46</td>", page)    # sales total
        self.assertIn("<td>Total</td>", page)
        self.assertIn("3 rows x 3 columns", page)

    def test_build_html_escapes_content(self):
        page = build_html(["a"], [["<b>&amp;"]])
        self.assertIn("&lt;b&gt;&amp;amp;", page)
        self.assertNotIn("<b>&amp;", page.replace("&lt;b&gt;&amp;amp;", ""))

    def test_build_html_no_totals(self):
        page = build_html(HEADER, ROWS, show_totals=False)
        self.assertNotIn('class="total"', page)
        self.assertIn("<table>", page)

    def test_build_html_empty_rows(self):
        page = build_html(HEADER, [])
        self.assertIn("0 rows x 3 columns", page)
        self.assertIn("<table>", page)

    def test_read_csv(self):
        path = "/tmp/test-report-input.csv"
        with open(path, "w", newline="") as fh:
            fh.write("name,visits\nAlpha,120\nBeta,80\n")
        try:
            header, rows = read_csv(path)
            self.assertEqual(header, ["name", "visits"])
            self.assertEqual(rows, [["Alpha", "120"], ["Beta", "80"]])
        finally:
            os.remove(path)

    def test_full_page_is_valid_html(self):
        page = build_html(HEADER, ROWS)
        self.assertTrue(page.startswith("<!DOCTYPE html>"))
        self.assertIn("</html>", page)
        self.assertIn("<thead>", page)
        self.assertIn("<tbody>", page)


if __name__ == "__main__":
    unittest.main(verbosity=2)
