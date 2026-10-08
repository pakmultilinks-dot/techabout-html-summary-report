# HTML Summary Report

A small Python script that turns a small CSV into a simple HTML report
with a table and totals. Built for TechAbout task 6 (ZR-26-00754).

## What it does

Given any CSV file (first row is the header), it builds a clean, styled
HTML page containing:

- the data as a table (zebra-striped rows, styled header)
- a totals row: numeric columns are summed, the first column is labeled
  "Total"
- a summary line (row x column count, generation date) and a footer note

All cell content is HTML-escaped, so stray `<`, `>`, `&` in the data
cannot break the page.

## Usage

```bash
python html_summary_report.py data.csv --output report.html
python html_summary_report.py data.csv --output report.html --title "My Report"
python html_summary_report.py data.csv --output report.html --no-totals
```

## Sample report

`sample/url-check-results.csv` is the real results CSV from the
URL Status Checker task (8 URLs checked). `sample/report.html` is the
generated report:

- 8 rows x 7 columns rendered as a styled table
- totals row sums the numeric columns (status codes, response times)

Open `sample/report.html` in any browser to view it.

## Tests

```bash
python test_html_summary_report.py
```

11 tests covering number detection, numeric-column detection, totals
(sum of ints and floats), HTML escaping, the totals-row toggle, empty
input, CSV reading, and overall page structure.

## Files

| File | Purpose |
|---|---|
| `html_summary_report.py` | The script |
| `test_html_summary_report.py` | 11 unit tests |
| `sample/url-check-results.csv` | Sample input CSV |
| `sample/report.html` | Sample HTML report |
