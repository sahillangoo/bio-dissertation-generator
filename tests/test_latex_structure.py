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
    """T1-LATEX-01: Verify dissertation.tex includes preamble and the kept front-matter pages."""
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

    for module in EXPECTED_FRONTMATTER_FILES:
        stem = module.replace(".tex", "")
        assert re.search(rf"\\(?:input|include)\s*\{{[^}}]*frontmatter/{stem}", content), (
            f"dissertation.tex does not include frontmatter/{stem}"
        )

    for module in EXPECTED_CHAPTER_FILES:
        stem = module.replace(".tex", "")
        assert re.search(rf"\\(?:input|include)\s*\{{[^}}]*chapters/{stem}", content), (
            f"dissertation.tex does not include chapters/{stem}"
        )

    for module in EXPECTED_APPENDIX_FILES:
        stem = module.replace(".tex", "")
        assert re.search(rf"\\(?:input|include)\s*\{{[^}}]*appendices/{stem}", content), (
            f"dissertation.tex does not include appendices/{stem}"
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


def test_frontmatter_certificate_and_declaration(project_root):
    """T1-LATEX-03: Certificate and declaration name the candidate and Kashmir Zoology department."""
    cert = (project_root / "frontmatter" / "certificate.tex").read_text(encoding="utf-8").lower()
    decl = (project_root / "frontmatter" / "declaration.tex").read_text(encoding="utf-8").lower()
    for keyword in ["bazilla", "24061119001", "kashmir", "zoology"]:
        assert keyword in cert, f"Keyword '{keyword}' missing in certificate.tex"
        assert keyword in decl, f"Keyword '{keyword}' missing in declaration.tex"


def test_chapter_modules_exist_for_kashmir_thesis(project_root):
    """T1-LATEX-04: Live Kashmir chapter files exist and are non-empty."""
    ch_dir = project_root / "chapters"
    assert ch_dir.is_dir(), f"Chapter directory missing: {ch_dir}"
    for name in EXPECTED_CHAPTER_FILES:
        path = ch_dir / name
        assert path.exists(), f"Missing chapter file: {path}"
        assert path.stat().st_size > 200, f"Chapter file too small: {path}"


def test_appendix_modules_exist_for_kashmir_thesis(project_root):
    """T1-LATEX-05: Raw ZOI appendix exists."""
    app_dir = project_root / "appendices"
    assert app_dir.is_dir(), f"Appendix directory missing: {app_dir}"
    path = app_dir / "appendix_a_zoi.tex"
    assert path.exists() and path.stat().st_size > 100


def test_master_references_bib_validity(project_root):
    """T1-LATEX-06: references.bib holds the live Kashmir bibliography."""
    bib_file = project_root / "references.bib"
    assert bib_file.exists(), f"Master references.bib missing at {bib_file}"
    keys = extract_bibtex_keys(bib_file)
    assert len(keys) >= 15, (
        f"references.bib contains only {len(keys)} entries; expected a populated bibliography"
    )


def test_in_vitro_title_casing(project_root):
    """KU Zoology registers: cover capitals, header title case, cites sentence case; in vitro always italic lowercase."""
    header = r"Antibacterial Potential of \textit{Dipsacus inermis}: An \textit{in vitro} Study"
    cover = r"ANTIBACTERIAL POTENTIAL OF\\ \textit{Dipsacus inermis}:\\ AN \textit{in vitro} STUDY"
    cited = r"Antibacterial potential of \textit{Dipsacus inermis}: an \textit{in vitro} study"
    title = (project_root / "frontmatter" / "title.tex").read_text(encoding="utf-8")
    cert = (project_root / "frontmatter" / "certificate.tex").read_text(encoding="utf-8")
    decl = (project_root / "frontmatter" / "declaration.tex").read_text(encoding="utf-8")
    acks = (project_root / "frontmatter" / "acknowledgements.tex").read_text(encoding="utf-8")
    preamble = (project_root / "preamble.tex").read_text(encoding="utf-8")
    for label, text in (
        ("title", title),
        ("certificate", cert),
        ("declaration", decl),
        ("acknowledgements", acks),
        ("preamble", preamble),
    ):
        assert "IN VITRO" not in text, f"all-caps IN VITRO found in {label}"
        assert "In Vitro" not in text, f"title-cased In Vitro found in {label}"
    assert r"\distitlecover" in title
    assert cover in preamble
    assert header in preamble
    assert cited in preamble
    assert r"\distitlecite" in cert
    assert r"\distitlecite" in decl
    assert r"\distitlecite" in acks
    assert r"\disshorttitle" in preamble
    assert r"\makebox[\headwidth]" in preamble
    assert r"Enrollment No.\ \disroll" in preamble
    assert r"AN \textit{in vitro} STUDY\\" not in preamble


# ============================================================================
# TIER 2: BOUNDARY & CORNER CASES (CITATION RESOLUTION & BIB INTEGRITY)
# ============================================================================

def test_all_cited_keys_resolved_in_references_bib(project_root):
    """T2-BIB-01: Verify all keys cited across all .tex files exist in references.bib."""
    bib_file = project_root / "references.bib"
    if not bib_file.exists():
        pytest.skip("references.bib not yet implemented")

    defined_keys = extract_bibtex_keys(bib_file)

    # Scan only the live Kashmir thesis files currently included in the root document.
    all_tex_files = [
        project_root / "dissertation.tex",
        *[project_root / "frontmatter" / f for f in EXPECTED_FRONTMATTER_FILES],
        *[project_root / "chapters" / f for f in EXPECTED_CHAPTER_FILES],
        *[project_root / "appendices" / f for f in EXPECTED_APPENDIX_FILES],
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


def test_final_result_plate_is_included(project_root):
    """Results chapter includes the incubated dual-plate photograph."""
    results = (project_root / "chapters" / "04_results.tex").read_text(encoding="utf-8")
    plate = project_root / "figures" / "fig11_final_result_plates.png"
    assert plate.exists() and plate.stat().st_size > 1000
    assert "fig11_final_result_plates.png" in results
    assert r"\label{fig:finalplates}" in results
    assert "agarplate-final-result-fig" not in results

