#!/usr/bin/env python3
"""
format_table.py - Tabular Data to LaTeX Booktabs & SIunitx Converter

Converts CSV and TSV files into publication-grade LaTeX tables adhering to
life sciences formatting standards (booktabs horizontal rules, no vertical rules,
and siunitx numeric alignment).
"""

import argparse
import csv
from pathlib import Path
import re
import sys
from typing import Any, List, Optional, Tuple


def is_numeric_value(val: str) -> bool:
    """Determine if a string represents a number (int or float)."""
    v = val.strip()
    if not v or v in ["-", "NA", "NaN", "?"]:
        return True  # Missing values are compatible with numeric columns
    try:
        float(v)
        return True
    except ValueError:
        return False


def get_numeric_format(values: List[str]) -> str:
    """Compute siunitx table-format string (e.g. 3.2) based on numeric column values."""
    max_int_digits = 1
    max_dec_digits = 0
    has_float = False

    for v in values:
        s = v.strip()
        if not s or s in ["-", "NA", "NaN", "?"]:
            continue
        try:
            f = float(s)
            if "." in s:
                has_float = True
                int_part, dec_part = s.split(".", 1)
                max_int_digits = max(max_int_digits, len(int_part.lstrip("-")))
                max_dec_digits = max(max_dec_digits, len(dec_part))
            else:
                max_int_digits = max(max_int_digits, len(s.lstrip("-")))
        except ValueError:
            pass

    if has_float:
        return f"table-format={max_int_digits}.{max_dec_digits}"
    return f"table-format={max_int_digits}"


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in plain text."""
    t = text.replace("&", "\\&").replace("%", "\\%").replace("$", "\\$")
    t = t.replace("#", "\\#").replace("_", "\\_")
    return t


def convert_csv_to_booktabs(
    csv_path: Path,
    caption: str = "Summary of morphological measurements.",
    label: str = "tab:morphometrics_table",
    longtable: bool = False,
) -> str:
    """Read CSV and produce publication-ready LaTeX table."""
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        # Detect delimiter
        first_line = f.readline()
        f.seek(0)
        delimiter = "\t" if "\t" in first_line else ","
        reader = list(csv.reader(f, delimiter=delimiter))

    if not reader:
        return "% Empty CSV file"

    headers = reader[0]
    data_rows = reader[1:]

    # Analyze columns
    num_cols = len(headers)
    col_is_numeric = []
    col_specs = []

    for col_idx in range(num_cols):
        col_values = [r[col_idx] for r in data_rows if col_idx < len(r)]
        all_numeric = all(is_numeric_value(v) for v in col_values) if col_values else False
        col_is_numeric.append(all_numeric)

        if all_numeric:
            fmt = get_numeric_format(col_values)
            col_specs.append(f"S[{fmt}]")
        else:
            col_specs.append("l")

    col_alignment = " ".join(col_specs)

    # Escape headers
    escaped_headers = []
    for h, is_num in zip(headers, col_is_numeric):
        clean_h = escape_latex(h)
        # In siunitx, non-numeric column headers in 'S' columns must be braced {Header}
        if is_num:
            escaped_headers.append(f"{{{clean_h}}}")
        else:
            escaped_headers.append(clean_h)
    header_line = " & ".join(escaped_headers) + " \\\\"

    # Format data rows
    body_lines = []
    for r in data_rows:
        row_cells = []
        for col_idx in range(num_cols):
            val = r[col_idx] if col_idx < len(r) else ""
            if col_is_numeric[col_idx]:
                val_clean = val.strip()
                if val_clean in ["-", "NA", "NaN", "?"]:
                    row_cells.append(f"{{{val_clean}}}")
                else:
                    row_cells.append(val_clean)
            else:
                row_cells.append(escape_latex(val.strip()))
        body_lines.append("  " + " & ".join(row_cells) + " \\\\")

    data_body = "\n".join(body_lines)

    if longtable:
        table_latex = f"""\\begin{{longtable}}{{{col_alignment}}}
\\caption{{{caption}}}\\label{{{label}}} \\\\
\\toprule
{header_line}
\\midrule
\\endfirsthead

\\multicolumn{{{num_cols}}}{{c}}{{\\tablename\\ \\thetable\\ -- Continued from previous page}} \\\\
\\toprule
{header_line}
\\midrule
\\endhead

\\midrule
\\multicolumn{{{num_cols}}}{{r}}{{\\textit{{Continued on next page}}}} \\\\
\\bottomrule
\\endfoot

\\bottomrule
\\endlastfoot

{data_body}
\\end{{longtable}}
"""
    else:
        table_latex = f"""\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
\\begin{{tabular}}{{{col_alignment}}}
\\toprule
{header_line}
\\midrule
{data_body}
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""
    return table_latex


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert CSV/TSV data into publication-standard LaTeX booktabs tables."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Input CSV or TSV file path",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file path for generated LaTeX table (prints to stdout if omitted)",
    )
    parser.add_argument(
        "--caption",
        "-c",
        type=str,
        default="Summary of morphological measurements.",
        help="Table caption",
    )
    parser.add_argument(
        "--label",
        "-l",
        type=str,
        default="tab:morphometrics_summary",
        help="Table label for cross-referencing",
    )
    parser.add_argument(
        "--longtable",
        action="store_true",
        help="Generate a multi-page longtable instead of standard tabular environment",
    )

    args = parser.parse_args()

    input_path = args.input.resolve()
    if not input_path.exists():
        sys.stderr.write(f"Error: Input file not found: {input_path}\n")
        return 1

    latex_code = convert_csv_to_booktabs(
        input_path,
        caption=args.caption,
        label=args.label,
        longtable=args.longtable,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(latex_code, encoding="utf-8")
        print(f"LaTeX table saved to {args.output}")
    else:
        print(latex_code)

    return 0


if __name__ == "__main__":
    sys.exit(main())
