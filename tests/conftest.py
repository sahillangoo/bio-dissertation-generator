"""
Shared fixtures and test utilities for the Biology & Zoology Dissertation Skill Suite test framework.
"""

import os
import re
import sys
import json
import shutil
import tempfile
from pathlib import Path
import pytest

# Workspace project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Expected Skills
EXPECTED_SKILLS = [
    "bio-research-sources",
    "bio-nomenclature-ethics",
    "bio-chapter-builder",
    "bio-reference-manager",
    "bio-scientific-formatting",
]

# Expected Staging Subdirectories
EXPECTED_STAGING_DIRS = [
    "existing_work",
    "papers",
    "citations",
    "notes",
]

# Expected Frontmatter Files (kept for the from-scratch rewrite)
EXPECTED_FRONTMATTER_FILES = [
    "title.tex",
    "certificate.tex",
    "declaration.tex",
    "acknowledgements.tex",
    "abstract.tex",
    "abbreviations.tex",
]

EXPECTED_CHAPTER_FILES = [
    "01_introduction.tex",
    "02_lit_review.tex",
    "03_methods.tex",
    "04_results.tex",
    "05_discussion.tex",
    "06_conclusion.tex",
]

EXPECTED_APPENDIX_FILES = [
    "appendix_a_zoi.tex",
]


def parse_yaml_frontmatter(file_path: Path) -> dict:
    """
    Parses YAML frontmatter from a markdown file delimited by '---'.
    Provides fallback parsing if PyYAML is not installed.
    """
    text = file_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"File {file_path} does not start with frontmatter delimiter '---'")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"File {file_path} does not have a closing '---' frontmatter delimiter")

    frontmatter_raw = parts[1].strip()

    # Try PyYAML if available
    try:
        import yaml
        data = yaml.safe_load(frontmatter_raw)
        if isinstance(data, dict):
            return data
    except ImportError:
        pass

    # Pure-Python robust fallback parser for frontmatter
    data = {}
    lines = frontmatter_raw.splitlines()
    current_key = None
    multiline_val = []
    in_folded = False

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if match and not (in_folded and (line.startswith("  ") or line.startswith("\t"))):
            if current_key and in_folded:
                data[current_key] = " ".join(multiline_val).strip()
                multiline_val = []
                in_folded = False
            current_key = match.group(1).strip()
            val = match.group(2).strip()
            if val in (">", ">-", "|", "|-"):
                in_folded = True
                multiline_val = []
            else:
                data[current_key] = val.strip("\"'")
        elif in_folded and current_key:
            multiline_val.append(stripped)

    if current_key and in_folded:
        data[current_key] = " ".join(multiline_val).strip()

    return data


def extract_bibtex_keys(bib_path: Path) -> set:
    """Extracts citation keys from a .bib file."""
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8")
    # Matches @type{key, ...
    keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)
    return set(keys)


def extract_tex_citations(tex_path: Path) -> set:
    r"""Extracts citation keys cited in a LaTeX file (\cite, \parencite, \textcite, \citep, \citet)."""
    if not tex_path.exists():
        return set()
    text = tex_path.read_text(encoding="utf-8", errors="ignore")
    # Matches \cite{key1,key2} or \parencite[...]{key1, key2}
    raw_citations = re.findall(r"\\(?:cite|parencite|textcite|citep|citet|autocite)(?:\[[^\]]*\])*\{([^}]+)\}", text)
    cited_keys = set()
    for citation_group in raw_citations:
        for key in citation_group.split(","):
            cleaned = key.strip()
            if cleaned:
                cited_keys.add(cleaned)
    return cited_keys


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def skills_dir(project_root) -> Path:
    return project_root / ".agents" / "skills"


@pytest.fixture(scope="session")
def staging_dir(project_root) -> Path:
    return project_root / "research_sources"
