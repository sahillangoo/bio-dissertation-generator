#!/usr/bin/env python3
"""
validate_nomenclature.py - ICZN Zoological Nomenclature and Animal Ethics Validator

Validates LaTeX and Markdown text for:
1. Unitalicized binomial and trinomial scientific names.
2. Lowercase genus names in scientific binomials.
3. Abbreviated genus names starting a sentence (e.g., "S. occidentalis...").
4. Zoological authority formatting (ICZN Art. 22A comma requirement).
5. Presence of mandatory IACUC / animal ethics statements in methods and frontmatter.
"""

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Tuple

# Common Latin species epithets in herpetology, zoology, and model systems
COMMON_EPITHETS = {
    "occidentalis", "graciosus", "stansburiana", "undulatus", "melanogaster",
    "elegans", "rerio", "musculus", "norvegicus", "sapiens", "lupus", "leo",
    "tigris", "carolinensis", "equestris", "sagrei", "punctatus", "viridis",
    "fuscus", "cinereus", "glutinosus", "horridus", "atrox", "adamanteus",
    "constrictor", "getula", "californiae", "pipiens", "catesbeiana", "clamitans"
}

# Known biological genera
KNOWN_GENERA = {
    "Sceloporus", "Uta", "Anolis", "Drosophila", "Caenorhabditis", "Danio",
    "Mus", "Rattus", "Homo", "Panthera", "Canis", "Plethodon", "Crotalus",
    "Lampropeltis", "Rana", "Lithobates", "Ambystoma", "Taricha", "Anopheles",
    "Aedes", "Xenopus"
}


def check_file_nomenclature(filepath: Path) -> List[Dict[str, Any]]:
    """Scan a file for ICZN nomenclature violations."""
    issues: List[Dict[str, Any]] = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        issues.append({
            "line": 0,
            "type": "read_error",
            "message": f"Could not read file: {e}",
            "severity": "error"
        })
        return issues

    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        # Ignore comments and preamble definitions
        stripped = line.strip()
        if stripped.startswith("%") or "\\newcommand" in line or "\\def" in line:
            continue

        # 1. Check for abbreviated genus at the start of a sentence
        # E.g., "^[A-Z]\. [a-z]+" or after period and space ". [A-Z]\. [a-z]+"
        abbrev_start = re.search(r'(?:^|[.!?]\s+)([A-Z]\.\s+[a-z]{3,})', line)
        if abbrev_start:
            token = abbrev_start.group(1)
            issues.append({
                "line": idx,
                "file": str(filepath),
                "type": "abbreviated_genus_at_sentence_start",
                "matched": token,
                "severity": "warning",
                "message": (
                    f"Abbreviated genus '{token}' starts a sentence. "
                    "Spell out the full genus at the beginning of a sentence per biological conventions."
                )
            })

        # 2. Check for lowercase genus names
        # E.g., "sceloporus occidentalis" or "\textit{sceloporus occidentalis}"
        lower_genus_matches = re.finditer(r'\b([a-z]+)\s+([a-z]{3,})\b', line)
        for m in lower_genus_matches:
            g_candidate = m.group(1).capitalize()
            e_candidate = m.group(2).lower()
            if g_candidate in KNOWN_GENERA and e_candidate in COMMON_EPITHETS:
                issues.append({
                    "line": idx,
                    "file": str(filepath),
                    "type": "lowercase_genus",
                    "matched": m.group(0),
                    "severity": "error",
                    "message": (
                        f"Genus name in '{m.group(0)}' must be capitalized ('{g_candidate} {e_candidate}')."
                    )
                })

        # 3. Check for unitalicized binomials
        # Search for known genus + epithet not wrapped in \textit, \emph, or \taxa
        for genus in KNOWN_GENERA:
            for epithet in COMMON_EPITHETS:
                target = f"{genus} {epithet}"
                if target in line:
                    # Check if enclosed in \textit{...}, \emph{...}, or \taxa{...}
                    pattern = rf'\\(textit|emph|taxa)\s*\{{[^}}]*{genus}\s+{epithet}[^}}]*\}}'
                    if not re.search(pattern, line):
                        # Also check if wrapped in markdown italics *Genus species* or _Genus species_
                        md_pattern = rf'[*_]{genus}\s+{epithet}[*_]'
                        if not re.search(md_pattern, line):
                            issues.append({
                                "line": idx,
                                "file": str(filepath),
                                "type": "unitalicized_binomial",
                                "matched": target,
                                "severity": "error",
                                "message": (
                                    f"Binomial taxon '{target}' appears unitalicized. "
                                    f"Wrap in \\textit{{{target}}} or \\taxa{{{target}}} (or *{target}* in Markdown)."
                                )
                            })

        # 4. Check for zoological authority formatting missing comma (ICZN Art. 22A)
        # E.g., "Sceloporus occidentalis Baird & Girard 1852" without comma before year
        auth_no_comma = re.search(r'([A-Z][a-z]+\s+[a-z]+)\s+([A-Z][a-zA-Z\s&]+?)\s+(\d{4})\b', line)
        if auth_no_comma:
            full_match = auth_no_comma.group(0)
            author = auth_no_comma.group(2).strip()
            year = auth_no_comma.group(3)
            # Make sure it's not preceded by a comma
            if not author.endswith(","):
                # Ensure author is not a common English word
                if author in ["Baird & Girard", "Linnaeus", "Girard", "Baird", "Holbrook"]:
                    issues.append({
                        "line": idx,
                        "file": str(filepath),
                        "type": "authority_missing_comma",
                        "matched": full_match,
                        "severity": "warning",
                        "message": (
                            f"Zoological authority in '{full_match}' is missing a comma before date. "
                            f"ICZN Art. 22A recommends: '{auth_no_comma.group(1)} {author}, {year}'."
                        )
                    })

    return issues


def check_ethics_statement(files: List[Path]) -> List[Dict[str, Any]]:
    """Verify presence of mandatory IACUC/ethics statement in methods or frontmatter."""
    issues = []
    found_iacuc = False
    methods_or_ethics_files = []

    for f in files:
        fname = f.name.lower()
        if "method" in fname or "ethics" in fname or "frontmatter" in str(f).lower():
            methods_or_ethics_files.append(f)
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
                if re.search(r'\b(IACUC|Animal Care and Use|protocol|permit|ASIH)\b', text, re.IGNORECASE):
                    found_iacuc = True
            except Exception:
                pass

    if not found_iacuc and methods_or_ethics_files:
        issues.append({
            "line": 1,
            "file": str(methods_or_ethics_files[0]),
            "type": "missing_ethics_statement",
            "matched": "IACUC Statement",
            "severity": "error",
            "message": (
                "No IACUC or animal care and use statement found in methods or ethics files. "
                "Life sciences dissertations involving vertebrates require explicit institutional protocol citation."
            )
        })

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ICZN zoological nomenclature and animal ethics compliance in dissertation files."
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        help="Path to a single file to validate",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        default=Path("."),
        help="Directory to scan for LaTeX and Markdown files (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail with exit code 1 if any warning or error is detected",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    args = parser.parse_args()

    files_to_check: List[Path] = []
    if args.file:
        files_to_check.append(args.file.resolve())
    else:
        root_dir = args.dir.resolve()
        for ext in [".tex", ".md", ".markdown"]:
            files_to_check.extend(root_dir.glob(f"**/*{ext}"))

    # Exclude files in .git and build directories
    filtered_files = [
        f for f in files_to_check
        if ".git" not in f.parts and "build" not in f.parts and ".tectonic" not in f.parts
    ]

    all_issues: List[Dict[str, Any]] = []
    for f in sorted(filtered_files):
        all_issues.extend(check_file_nomenclature(f))

    # Run ethics compliance check
    all_issues.extend(check_ethics_statement(filtered_files))

    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]

    if args.json:
        result = {
            "total_files_scanned": len(filtered_files),
            "total_issues": len(all_issues),
            "errors": len(errors),
            "warnings": len(warnings),
            "issues": all_issues,
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Scanned {len(filtered_files)} file(s). Found {len(errors)} error(s), {len(warnings)} warning(s).\n")
        for iss in all_issues:
            icon = "❌ ERROR" if iss["severity"] == "error" else "⚠️ WARN "
            rel_file = iss.get("file", "unknown")
            print(f"{icon} [{rel_file}:{iss['line']}] ({iss['type']}): {iss['message']}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
