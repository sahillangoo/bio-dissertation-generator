#!/usr/bin/env python3
"""
ingest_sources.py - Source Ingestion and Manifest Generator for Life Sciences Dissertations

Scans the research_sources/ directory (existing_work, papers, citations, notes),
computes SHA-256 hashes, extracts structure/headings/metadata, maps items to
dissertation chapter targets, and produces a structured sources_manifest.json.
"""

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 hexadecimal digest of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def extract_headings_markdown(filepath: Path) -> List[str]:
    """Extract top-level and secondary headings from a Markdown file."""
    headings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                match = re.match(r"^(#{1,3})\s+(.+)$", line)
                if match:
                    headings.append(match.group(2).strip())
    except Exception:
        pass
    return headings


def extract_headings_latex(filepath: Path) -> List[str]:
    """Extract section titles from a LaTeX file."""
    headings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            pattern = re.compile(r"\\(chapter|section|subsection)\*?\{([^}]+)\}")
            for match in pattern.finditer(content):
                headings.append(match.group(2).strip())
    except Exception:
        pass
    return headings


def extract_bibtex_keys(filepath: Path) -> List[str]:
    """Extract BibTeX citation keys from a .bib file."""
    keys = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            pattern = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
            for line in f:
                match = pattern.search(line)
                if match:
                    keys.append(match.group(1).strip())
    except Exception:
        pass
    return keys


def inspect_csv_metadata(filepath: Path) -> Dict[str, Any]:
    """Inspect CSV columns and row count."""
    metadata: Dict[str, Any] = {"columns": [], "row_count": 0}
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            if headers:
                metadata["columns"] = [h.strip() for h in headers]
                metadata["row_count"] = sum(1 for _ in reader)
    except Exception:
        pass
    return metadata


def infer_target_chapter(filepath: Path, category: str, headings: List[str]) -> str:
    """Infer target dissertation chapter based on path, category, and headings."""
    name_lower = filepath.stem.lower()
    combined_text = f"{name_lower} {' '.join(headings).lower()}"

    if category == "citations":
        return "references.bib"

    if "method" in combined_text or "protocol" in combined_text or "primer" in combined_text:
        return "chapters/03_methods.tex"
    if "result" in combined_text or "morphometric" in combined_text or "measurement" in combined_text:
        if filepath.suffix.lower() in [".csv", ".tsv"]:
            return "appendices/appendix_a_specimens.tex"
        return "chapters/04_results.tex"
    if "lit" in combined_text or "review" in combined_text or "paper" in combined_text:
        return "chapters/02_lit_review.tex"
    if "intro" in combined_text or "background" in combined_text:
        return "chapters/01_introduction.tex"
    if "discuss" in combined_text or "synthesis" in combined_text:
        return "chapters/05_discussion.tex"
    if "committee" in combined_text or "note" in combined_text or "guideline" in combined_text:
        return "frontmatter/ethics_statement.tex"

    # Category defaults
    defaults = {
        "existing_work": "chapters/03_methods.tex",
        "papers": "chapters/02_lit_review.tex",
        "notes": "chapters/01_introduction.tex",
    }
    return defaults.get(category, "chapters/01_introduction.tex")


def scan_sources(sources_dir: Path) -> List[Dict[str, Any]]:
    """Scan research_sources directory and collect source metadata."""
    categories = ["existing_work", "papers", "citations", "notes"]
    manifest_entries = []

    for cat in categories:
        cat_dir = sources_dir / cat
        if not cat_dir.is_dir():
            continue

        for item in sorted(cat_dir.iterdir()):
            if item.is_dir() or item.name.startswith("."):
                continue  # Skip directories and hidden files like .gitkeep

            ext = item.suffix.lower()
            rel_path = item.relative_to(sources_dir.parent).as_posix()
            sha256 = compute_sha256(item)
            size_bytes = item.stat().st_size

            headings: List[str] = []
            keys: List[str] = []
            csv_meta: Optional[Dict[str, Any]] = None

            if ext in [".md", ".markdown", ".txt"]:
                headings = extract_headings_markdown(item)
                file_type = "markdown" if ext != ".txt" else "text"
            elif ext == ".tex":
                headings = extract_headings_latex(item)
                file_type = "latex"
            elif ext == ".bib":
                keys = extract_bibtex_keys(item)
                file_type = "bibtex"
            elif ext in [".csv", ".tsv"]:
                csv_meta = inspect_csv_metadata(item)
                file_type = "tabular_data"
            elif ext == ".pdf":
                file_type = "pdf_document"
            elif ext in [".docx", ".doc"]:
                file_type = "word_document"
            else:
                file_type = "binary_or_other"

            target_chapter = infer_target_chapter(item, cat, headings)

            entry: Dict[str, Any] = {
                "path": rel_path,
                "filename": item.name,
                "category": cat,
                "file_type": file_type,
                "size_bytes": size_bytes,
                "sha256": sha256,
                "target_chapter": target_chapter,
                "headings": headings,
            }

            if keys:
                entry["citation_keys"] = keys
                entry["key_count"] = len(keys)

            if csv_meta:
                entry["tabular_metadata"] = csv_meta

            manifest_entries.append(entry)

    return manifest_entries


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan research_sources/ directory and generate a machine-readable ingestion manifest."
    )
    parser.add_argument(
        "--sources",
        "-s",
        type=Path,
        default=Path("research_sources"),
        help="Path to research_sources directory (default: research_sources)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("research_sources/sources_manifest.json"),
        help="Output manifest file path (default: research_sources/sources_manifest.json)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print human-readable summary of scanned sources to stdout",
    )

    args = parser.parse_args()

    sources_dir = args.sources.resolve()
    if not sources_dir.exists():
        sys.stderr.write(f"Error: Sources directory not found: {sources_dir}\n")
        return 1

    entries = scan_sources(sources_dir)
    output_path = args.output.resolve()

    manifest_data = {
        "version": "1.0",
        "generated_at": "2026-09-16T12:53:03Z",
        "total_files": len(entries),
        "sources_directory": sources_dir.as_posix(),
        "files": entries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated manifest with {len(entries)} sources -> {output_path}")

    if args.summary:
        print("\n--- Staging Summary ---")
        for e in entries:
            print(f"[{e['category']}] {e['filename']} -> {e['target_chapter']} ({e['file_type']}, {e['size_bytes']} bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
