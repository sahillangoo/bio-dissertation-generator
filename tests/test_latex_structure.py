"""
Tier 1 and Tier 2 Tests: Modular LaTeX Dissertation Template & Bibliography Validation.
Verifies LaTeX root document, preamble macros, modular structure, and citation key integrity.
"""

import os
import re
from pathlib import Path
import pytest

from conftest import (
    EXPECTED_FRONTMATTER_FILES,
    EXPECTED_CHAPTER_FILES,
    EXPECTED_APPENDIX_FILES,
    extract_bibtex_keys,
    extract_tex_citations,
)


# ============================================================================
# TIER 1: FEATURE COVERAGE (LATEX ARCHITECTURE)
# ============================================================================

def test_dissertation_root_document_exists(project_root):
    """T1-LATEX-01: Verify dissertation.tex exists at project root."""
    root_tex = project_root / "dissertation.tex"
    assert root_tex.exists(), f"Master root document missing: {root_tex}"
    assert root_tex.is_file(), f"{root_tex} is not a regular file"
    assert root_tex.stat().st_size > 100, f"{root_tex} is too small (< 100 bytes)"


def test_dissertation_root_includes_modular_components(project_root):
    """T1-LATEX-01: Verify dissertation.tex includes preamble, frontmatter, chapters, and bibliography."""
    root_tex = project_root / "dissertation.tex"
    if not root_tex.exists():
        pytest.skip("dissertation.tex not yet implemented")

    content = root_tex.read_text(encoding="utf-8")

    # Document class check
    assert r"\documentclass" in content, "Missing \\documentclass in dissertation.tex"

    # Preamble input check
    assert re.search(r"\\input\s*\{[^}]*preamble", content), (
        "dissertation.tex does not input preamble.tex"
    )

    # Core modular inputs
    for module_pattern in ["frontmatter", "chapters", "appendices"]:
        assert re.search(rf"\\(?:input|include)\s*\{{[^}}]*{module_pattern}", content), (
            f"dissertation.tex does not include {module_pattern} module"
        )
    assert re.search(r"\\(?:printbibliography|addbibresource|bibliography)", content), (
        "dissertation.tex does not include bibliography command (printbibliography / addbibresource)"
    )


def test_preamble_loads_required_life_sciences_packages(project_root):
    """T1-LATEX-02: Verify preamble.tex loads geometry, booktabs, siunitx, mhchem, forest, biblatex."""
    preamble_path = project_root / "preamble.tex"
    assert preamble_path.exists(), f"preamble.tex missing at {preamble_path}"

    content = preamble_path.read_text(encoding="utf-8")
    required_packages = [
        "geometry",
        "booktabs",
        "siunitx",
        "mhchem",
        "forest",
        "biblatex",
    ]

    for pkg in required_packages:
        assert re.search(rf"\\usepackage(?:\[[^\]]*\])?\{{{pkg}\}}", content), (
            f"Required package '{pkg}' not loaded in preamble.tex"
        )


def test_preamble_defines_iczn_zoological_macros(project_root):
    r"""T1-LATEX-02: Verify preamble.tex defines ICZN macros: \taxa, \taxonauth, \spnov, \holotype."""
    preamble_path = project_root / "preamble.tex"
    assert preamble_path.exists(), f"preamble.tex missing at {preamble_path}"

    content = preamble_path.read_text(encoding="utf-8")
    required_macros = [r"\taxa", r"\taxonauth", r"\spnov", r"\holotype"]

    for macro in required_macros:
        assert macro in content, f"ICZN macro '{macro}' not defined in preamble.tex"


@pytest.mark.parametrize("fm_filename", EXPECTED_FRONTMATTER_FILES)
def test_frontmatter_modules_exist(project_root, fm_filename):
    """T1-LATEX-03: Verify all expected frontmatter modules exist in frontmatter/."""
    fm_file = project_root / "frontmatter" / fm_filename
    assert fm_file.exists(), f"Frontmatter module missing: {fm_file}"
    assert fm_file.stat().st_size > 0, f"Frontmatter module is empty: {fm_file}"


def test_frontmatter_ethics_statement_content(project_root):
    """T1-LATEX-03: Verify ethics_statement.tex contains IACUC / animal ethics compliance terms."""
    ethics_file = project_root / "frontmatter" / "ethics_statement.tex"
    assert ethics_file.exists(), f"ethics_statement.tex missing at {ethics_file}"

    content = ethics_file.read_text(encoding="utf-8").lower()
    for keyword in ["iacuc", "animal", "protocol"]:
        assert keyword in content, (
            f"Keyword '{keyword}' missing in ethics_statement.tex"
        )


@pytest.mark.parametrize("ch_filename", EXPECTED_CHAPTER_FILES)
def test_chapter_modules_exist(project_root, ch_filename):
    """T1-LATEX-04: Verify all 5 modular chapter files exist in chapters/."""
    ch_file = project_root / "chapters" / ch_filename
    assert ch_file.exists(), f"Chapter module missing: {ch_file}"
    assert ch_file.stat().st_size > 0, f"Chapter module is empty: {ch_file}"


@pytest.mark.parametrize("app_filename", EXPECTED_APPENDIX_FILES)
def test_appendix_modules_exist(project_root, app_filename):
    """T1-LATEX-05: Verify all appendix files exist in appendices/."""
    app_file = project_root / "appendices" / app_filename
    assert app_file.exists(), f"Appendix module missing: {app_file}"
    assert app_file.stat().st_size > 0, f"Appendix module is empty: {app_file}"


def test_master_references_bib_validity(project_root):
    """T1-LATEX-06: Verify references.bib exists and contains valid BibTeX entries."""
    bib_file = project_root / "references.bib"
    assert bib_file.exists(), f"Master references.bib missing at {bib_file}"
    assert bib_file.stat().st_size > 0, f"{bib_file} is empty"

    keys = extract_bibtex_keys(bib_file)
    assert len(keys) >= 5, f"references.bib contains too few entries ({len(keys)} found, expected >= 5)"


# ============================================================================
# TIER 2: BOUNDARY & CORNER CASES (CITATION RESOLUTION & BIB INTEGRITY)
# ============================================================================

def test_all_cited_keys_resolved_in_references_bib(project_root):
    """T2-BIB-01: Verify all keys cited across all .tex files exist in references.bib."""
    bib_file = project_root / "references.bib"
    if not bib_file.exists():
        pytest.skip("references.bib not yet implemented")

    defined_keys = extract_bibtex_keys(bib_file)
    assert len(defined_keys) > 0, "No keys found in references.bib"

    # Scan all .tex files in project
    all_tex_files = [
        project_root / "dissertation.tex",
        *list((project_root / "frontmatter").glob("*.tex")),
        *list((project_root / "chapters").glob("*.tex")),
        *list((project_root / "appendices").glob("*.tex")),
    ]

    missing_citations = {}
    for tex_file in all_tex_files:
        if not tex_file.exists():
            continue
        cited = extract_tex_citations(tex_file)
        unresolved = cited - defined_keys
        if unresolved:
            missing_citations[tex_file.name] = unresolved

    assert not missing_citations, (
        f"Found undefined citation keys that would trigger compilation warnings:\n"
        f"{missing_citations}"
    )


def test_citation_extractor_detects_synthetic_missing_key(tmp_path):
    """T2-BIB-01: Verify extraction utility correctly detects a missing synthetic citation key."""
    fake_tex = tmp_path / "fake_chapter.tex"
    fake_tex.write_text(r"According to \parencite{darwin1859} and \textcite{unresolved_author_2099}.", encoding="utf-8")
    cited = extract_tex_citations(fake_tex)
    assert "darwin1859" in cited
    assert "unresolved_author_2099" in cited

    defined = {"darwin1859"}
    missing = cited - defined
    assert missing == {"unresolved_author_2099"}
