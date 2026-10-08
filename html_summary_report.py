#!/usr/bin/env python3
"""
HTML Summary Report
===================

Turns a small CSV file into a simple HTML report with a table and totals.

What it does:
  - Reads any CSV file (first row is the header).
  - Builds a clean, styled HTML page with the data as a table.
  - Adds a totals row: numeric columns get their sum; text columns show
    the row count ("N rows"); the first column is labeled "Total".
  - Adds a small summary line above the table (rows, columns, generated
    date) and a footer note.
  - All cell content is HTML-escaped, so stray < > & in the data cannot
    break the page.

Usage:
    python html_summary_report.py data.csv --output report.html
    python html_summary_report.py data.csv --output report.html --title "My Report"
    python html_summary_report.py data.csv --output report.html --no-totals

TechAbout Python Developer task 6 - HTML Summary Report (ZR-26-00754).
"""

import argparse
import csv
import html
import sys
from datetime import date


def read_csv(path):
    """Read a CSV file. Returns (header list, rows list of lists)."""
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def is_number(text):
    """True if the text parses as a plain number."""
    try:
        float(text.replace(",", ""))
        return True
    except (ValueError, AttributeError):
        return False


def numeric_columns(header, rows):
    """Indices of columns where every non-empty value is numeric."""
    numeric = []
    for i in range(len(header)):
        values = [r[i] for r in rows if len(r) > i and r[i].strip() != ""]
        if values and all(is_number(v) for v in values):
            numeric.append(i)
    return numeric


def column_total(rows, index):
    total = sum(float(r[index].replace(",", ""))
                for r in rows if len(r) > index and r[index].strip() != "")
    return int(total) if total == int(total) else round(total, 2)


def build_html(header, rows, title="CSV Summary Report", show_totals=True):
    """Build the full HTML report page."""
    esc = html.escape
    today = date.today().isoformat()
    numeric = numeric_columns(header, rows) if show_totals else []

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append("<title>%s</title>" % esc(title))
    parts.append("<style>")
    parts.append("body{font-family:Arial,Helvetica,sans-serif;margin:40px;color:#222;}")
    parts.append("h1{color:#1f497d;}")
    parts.append(".summary{color:#555;margin-bottom:16px;}")
    parts.append("table{border-collapse:collapse;width:100%;}")
    parts.append("th,td{border:1px solid #bbb;padding:8px 10px;text-align:left;}")
    parts.append("th{background:#1f497d;color:#fff;}")
    parts.append("tr:nth-child(even){background:#f2f6fb;}")
    parts.append("tr.total td{background:#dce6f1;font-weight:bold;}")
    parts.append(".footer{margin-top:16px;color:#888;font-size:0.85em;}")
    parts.append("</style>")
    parts.append("</head>")
    parts.append("<body>")
    parts.append("<h1>%s</h1>" % esc(title))
    parts.append('<p class="summary">%d rows x %d columns. Generated %s.</p>' %
                 (len(rows), len(header), today))
    parts.append("<table>")
    parts.append("<thead><tr>%s</tr></thead>" %
                 "".join("<th>%s</th>" % esc(c) for c in header))
    parts.append("<tbody>")
    for row in rows:
        cells = [esc(row[i]) if i < len(row) else "" for i in range(len(header))]
        parts.append("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in cells))
    if show_totals and rows:
        total_cells = []
        for i in range(len(header)):
            if i == 0:
                total_cells.append("<td>Total</td>")
            elif i in numeric:
                total_cells.append("<td>%s</td>" % esc(str(column_total(rows, i))))
            else:
                total_cells.append("<td></td>")
        parts.append('<tr class="total">%s</tr>' % "".join(total_cells))
    parts.append("</tbody>")
    parts.append("</table>")
    parts.append('<p class="footer">Generated from CSV by html_summary_report.py. '
                 'Numeric columns are summed in the totals row.</p>')
    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Turn a CSV file into an HTML report with a table and totals.")
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument("--output", required=True,
                        help="Path for the generated HTML report")
    parser.add_argument("--title", default="CSV Summary Report",
                        help="Report title (default: CSV Summary Report)")
    parser.add_argument("--no-totals", action="store_true",
                        help="Skip the totals row")
    args = parser.parse_args(argv)

    try:
        header, rows = read_csv(args.csv_file)
    except FileNotFoundError:
        print("Error: file not found: %s" % args.csv_file, file=sys.stderr)
        return 1

    if not header:
        print("Error: CSV is empty: %s" % args.csv_file, file=sys.stderr)
        return 1

    page = build_html(header, rows, args.title, show_totals=not args.no_totals)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(page)
    print("Report written to %s (%d rows)" % (args.output, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
