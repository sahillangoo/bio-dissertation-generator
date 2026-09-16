#!/usr/bin/env python3
"""
bib_manager.py - BibLaTeX Reference Manager and Citation Validator for Life Sciences

Capabilities:
1. Validates BibTeX files for syntax errors and missing required fields.
2. Merges and deduplicates multiple BibTeX files (by DOI, key, or title) into master references.bib.
3. Checks LaTeX files for undefined citation keys referenced via \\cite, \\citep, \\textcite, etc.
"""

import argparse
from collections import OrderedDict
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple


class BibEntry:
    def __init__(self, entry_type: str, key: str, fields: Dict[str, str], raw_text: str = ""):
        self.entry_type = entry_type.lower()
        self.key = key.strip()
        self.fields = {k.lower(): v.strip() for k, v in fields.items()}
        self.raw_text = raw_text

    @property
    def doi(self) -> Optional[str]:
        val = self.fields.get("doi", "").strip()
        if val:
            val = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", val, flags=re.IGNORECASE)
            return val.lower()
        return None

    @property
    def title(self) -> str:
        t = self.fields.get("title", "")
        # Remove LaTeX commands, braces, and excess whitespace
        t = re.sub(r"\\[a-zA-Z]+", "", t)
        t = re.sub(r"[{}]", "", t)
        return " ".join(t.lower().split())

    @property
    def author(self) -> str:
        return self.fields.get("author", "")

    @property
    def year(self) -> str:
        return self.fields.get("year", "")

    def format_bibtex(self) -> str:
        """Format entry as clean BibTeX string."""
        lines = [f"@{self.entry_type}{{{self.key},"]
        # Standard field order for life sciences
        preferred_order = [
            "author", "title", "journal", "booktitle", "editor",
            "year", "volume", "number", "pages", "edition",
            "publisher", "address", "doi", "url", "note"
        ]
        written_fields = set()
        for field in preferred_order:
            if field in self.fields:
                val = self.fields[field]
                lines.append(f"  {field:<12} = {{{val}}},")
                written_fields.add(field)

        for field, val in sorted(self.fields.items()):
            if field not in written_fields:
                lines.append(f"  {field:<12} = {{{val}}},")

        # Strip trailing comma from last field line
        if len(lines) > 1:
            lines[-1] = lines[-1].rstrip(",")
        lines.append("}\n")
        return "\n".join(lines)


def parse_bibtex_file(filepath: Path) -> List[BibEntry]:
    """Parse BibTeX entries from file using regex and brace matching."""
    entries: List[BibEntry] = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        sys.stderr.write(f"Error reading {filepath}: {e}\n")
        return entries

    # Match @type{key, ... }
    entry_pattern = re.compile(r"@([a-zA-Z]+)\s*\{\s*([^,]+)\s*,", re.MULTILINE)
    pos = 0

    while True:
        match = entry_pattern.search(content, pos)
        if not match:
            break

        entry_type = match.group(1).lower()
        key = match.group(2).strip()

        # Skip non-entry macros like @string, @comment, @preamble
        if entry_type in ["string", "comment", "preamble"]:
            pos = match.end()
            continue

        # Find matching closing brace
        start_idx = match.end()
        brace_depth = 1
        curr = start_idx
        while curr < len(content) and brace_depth > 0:
            ch = content[curr]
            if ch == "{":
                brace_depth += 1
            elif ch == "}":
                brace_depth -= 1
            curr += 1

        body = content[start_idx : curr - 1]
        raw_text = content[match.start() : curr]
        pos = curr

        # Parse key-value fields inside the body
        fields: Dict[str, str] = {}
        # Pattern for field = {value} or field = "value" or field = 123
        field_matches = re.finditer(
            r'([a-zA-Z_-]+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"([^"]*)"|([0-9]+))',
            body
        )
        for fm in field_matches:
            fname = fm.group(1).strip().lower()
            fval = fm.group(2) or fm.group(3) or fm.group(4) or ""
            fields[fname] = fval.strip()

        entries.append(BibEntry(entry_type, key, fields, raw_text))

    return entries


def validate_bib_entries(entries: List[BibEntry]) -> Tuple[List[str], List[str]]:
    """Validate entries for required fields and key formatting."""
    errors = []
    warnings = []
    seen_keys: Set[str] = set()

    for entry in entries:
        # Check duplicate key
        if entry.key in seen_keys:
            errors.append(f"Duplicate citation key detected: '{entry.key}'")
        seen_keys.add(entry.key)

        # Check required fields
        if not entry.year:
            warnings.append(f"Entry '{entry.key}' missing 'year' field")
        if not entry.title:
            errors.append(f"Entry '{entry.key}' missing 'title' field")

        if entry.entry_type in ["article", "book", "phdthesis", "mastersthesis"]:
            if not entry.author and not entry.fields.get("editor"):
                errors.append(f"Entry '{entry.key}' missing 'author' or 'editor' field")

        if entry.entry_type == "article" and not entry.fields.get("journal"):
            warnings.append(f"Article '{entry.key}' missing 'journal' field")

    return errors, warnings


def merge_bib_files(input_paths: List[Path], master_path: Path, sort_keys: bool = True) -> int:
    """Merge entries from multiple files into master_path with deduplication."""
    existing_entries: List[BibEntry] = []
    if master_path.exists():
        existing_entries = parse_bibtex_file(master_path)

    all_entries: List[BibEntry] = list(existing_entries)
    for p in input_paths:
        if p == master_path:
            continue
        all_entries.extend(parse_bibtex_file(p))

    # Deduplicate: priority to existing keys, then DOIs, then normalized titles
    unique_entries: Dict[str, BibEntry] = OrderedDict()
    seen_dois: Set[str] = set()
    seen_titles: Set[str] = set()
    duplicates_removed = 0

    for entry in all_entries:
        # Check duplicate key
        if entry.key in unique_entries:
            duplicates_removed += 1
            continue

        # Check DOI
        if entry.doi and entry.doi in seen_dois:
            duplicates_removed += 1
            continue

        # Check title
        if entry.title and len(entry.title) > 10 and entry.title in seen_titles:
            duplicates_removed += 1
            continue

        # Add
        unique_entries[entry.key] = entry
        if entry.doi:
            seen_dois.add(entry.doi)
        if entry.title:
            seen_titles.add(entry.title)

    entries_to_write = list(unique_entries.values())
    if sort_keys:
        entries_to_write.sort(key=lambda e: e.key.lower())

    master_path.parent.mkdir(parents=True, exist_ok=True)
    with open(master_path, "w", encoding="utf-8") as f:
        f.write("% Master References Database for Biology & Zoology Dissertation\n")
        f.write("% Generated / Managed via bio-reference-manager (bib_manager.py)\n\n")
        for entry in entries_to_write:
            f.write(entry.format_bibtex() + "\n")

    print(f"Successfully merged into {master_path}: {len(entries_to_write)} unique entries ({duplicates_removed} duplicates skipped).")
    return 0


def check_citations_in_tex(tex_dir: Path, bib_path: Path) -> Tuple[Set[str], Set[str]]:
    """Compare citation keys in .tex files with keys in .bib file."""
    bib_entries = parse_bibtex_file(bib_path)
    defined_keys = {e.key for e in bib_entries}

    cited_keys: Set[str] = set()
    cite_pattern = re.compile(r"\\(?:cite|citep|citet|textcite|parencite|autocite|nocite)\*?\{([^}]+)\}")

    tex_files = list(tex_dir.glob("**/*.tex"))
    for tf in tex_files:
        if ".git" in tf.parts or "build" in tf.parts:
            continue
        try:
            content = tf.read_text(encoding="utf-8", errors="replace")
            for m in cite_pattern.finditer(content):
                raw_keys = m.group(1).split(",")
                for rk in raw_keys:
                    clean_k = rk.strip()
                    if clean_k:
                        cited_keys.add(clean_k)
        except Exception:
            pass

    missing_keys = cited_keys - defined_keys
    return cited_keys, missing_keys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="BibLaTeX reference database manager, validator, and merger for life sciences."
    )
    parser.add_argument(
        "--validate",
        "-v",
        type=Path,
        help="Validate a BibTeX file for syntax errors and missing required fields",
    )
    parser.add_argument(
        "--merge",
        "-m",
        action="store_true",
        help="Merge staged BibTeX files into master references.bib",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Input BibTeX file or directory of .bib files for merging",
    )
    parser.add_argument(
        "--master",
        type=Path,
        default=Path("references.bib"),
        help="Path to master references.bib file (default: references.bib)",
    )
    parser.add_argument(
        "--check-citations",
        action="store_true",
        help="Scan LaTeX files for citation keys and verify they exist in master references.bib",
    )
    parser.add_argument(
        "--tex-dir",
        type=Path,
        default=Path("."),
        help="Directory containing .tex files to check (default: .)",
    )

    args = parser.parse_args()

    if args.validate:
        filepath = args.validate.resolve()
        if not filepath.exists():
            sys.stderr.write(f"Error: File not found: {filepath}\n")
            return 1
        entries = parse_bibtex_file(filepath)
        errors, warnings = validate_bib_entries(entries)
        print(f"Validated {filepath}: parsed {len(entries)} entries.")
        for err in errors:
            print(f"❌ ERROR: {err}")
        for warn in warnings:
            print(f"⚠️ WARN: {warn}")
        return 1 if errors else 0

    if args.merge:
        if not args.input:
            sys.stderr.write("Error: --input required when using --merge\n")
            return 1
        input_path = args.input.resolve()
        master_path = args.master.resolve()

        bib_files = []
        if input_path.is_dir():
            bib_files = list(input_path.glob("**/*.bib"))
        elif input_path.is_file():
            bib_files = [input_path]

        if not bib_files:
            print(f"No .bib files found in {input_path}")
            return 0

        return merge_bib_files(bib_files, master_path)

    if args.check_citations:
        bib_path = args.master.resolve()
        tex_dir = args.tex_dir.resolve()
        if not bib_path.exists():
            sys.stderr.write(f"Error: Master bibliography not found: {bib_path}\n")
            return 1
        cited_keys, missing_keys = check_citations_in_tex(tex_dir, bib_path)
        print(f"Checked citations in {tex_dir}: found {len(cited_keys)} unique cited keys.")
        if missing_keys:
            print(f"❌ Missing keys ({len(missing_keys)}) in {bib_path.name}:")
            for mk in sorted(missing_keys):
                print(f"  - {mk}")
            return 1
        else:
            print(f"✅ All {len(cited_keys)} cited keys resolved successfully in {bib_path.name}.")
            return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
