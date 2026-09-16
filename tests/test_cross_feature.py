"""
Tier 3 Tests: Cross-Feature Interactions & Pipeline Data Flows.
Verifies integration across research staging, skill CLI tools, BibTeX merging, and LaTeX compilation.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import pytest


def test_ingest_sources_manifest_generation(project_root, tmp_path):
    """T3-INT-01: ingest_sources.py processes staging data and produces compliant sources_manifest.json."""
    script_path = (
        project_root
        / ".agents"
        / "skills"
        / "bio-research-sources"
        / "scripts"
        / "ingest_sources.py"
    )
    if not script_path.exists():
        pytest.skip(f"ingest_sources.py not yet implemented at {script_path}")

    staging_dir = project_root / "research_sources"
    manifest_out = tmp_path / "sources_manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--sources",
            str(staging_dir),
            "--output",
            str(manifest_out),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert result.returncode == 0, (
        f"ingest_sources.py failed with code {result.returncode}:\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )
    assert manifest_out.exists(), f"Output manifest not generated at {manifest_out}"

    manifest_data = json.loads(manifest_out.read_text(encoding="utf-8"))
    # Manifest should be an array of files or object containing files array
    files_list = manifest_data if isinstance(manifest_data, list) else manifest_data.get("files", [])
    assert len(files_list) > 0, "Manifest should contain at least one staged file entry"

    first_entry = files_list[0]
    for required_key in ["path", "sha256"]:
        assert required_key in first_entry, (
            f"Required key '{required_key}' missing in manifest entry: {first_entry}"
        )


def test_bib_manager_merge_and_deduplication(project_root, tmp_path):
    """T3-INT-02: bib_manager.py merges staged citations into master .bib with deduplication."""
    script_path = (
        project_root
        / ".agents"
        / "skills"
        / "bio-reference-manager"
        / "scripts"
        / "bib_manager.py"
    )
    if not script_path.exists():
        pytest.skip(f"bib_manager.py not yet implemented at {script_path}")

    # Create two temporary .bib files with one overlapping entry and two distinct entries
    input_dir = tmp_path / "citations_in"
    input_dir.mkdir()

    bib1 = input_dir / "user1.bib"
    bib1.write_text(
        """@article{darwin1859,
  author = {Darwin, Charles},
  title = {On the Origin of Species},
  year = {1859}
}
@article{smith2021,
  author = {Smith, John},
  title = {Phylogenetic Systematics of Carabidae},
  year = {2021}
}
""",
        encoding="utf-8",
    )

    bib2 = input_dir / "user2.bib"
    bib2.write_text(
        """@article{darwin1859,
  author = {Darwin, Charles},
  title = {On the Origin of Species (Duplicate)},
  year = {1859}
}
@article{jones2023,
  author = {Jones, Alice},
  title = {Morphological Variation in Heliconius},
  year = {2023}
}
""",
        encoding="utf-8",
    )

    master_out = tmp_path / "references_merged.bib"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--merge",
            "--input",
            str(input_dir),
            "--master",
            str(master_out),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )

    assert result.returncode == 0, (
        f"bib_manager.py failed with code {result.returncode}:\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )
    assert master_out.exists(), f"Merged bib file was not created at {master_out}"

    merged_content = master_out.read_text(encoding="utf-8")
    assert "@article{darwin1859" in merged_content or "darwin1859" in merged_content
    assert "smith2021" in merged_content
    assert "jones2023" in merged_content

    # Assert darwin1859 is not duplicated
    assert merged_content.count("darwin1859,") <= 1, "Duplicate citation key found after merge"


def test_newick_to_forest_conversion(project_root, tmp_path):
    """T3-INT-03: newick_to_forest.py converts Newick strings into valid TikZ/Forest LaTeX."""
    script_path = (
        project_root
        / ".agents"
        / "skills"
        / "bio-scientific-formatting"
        / "scripts"
        / "newick_to_forest.py"
    )
    if not script_path.exists():
        pytest.skip(f"newick_to_forest.py not yet implemented at {script_path}")

    sample_newick = "((Panthera_leo:0.1,Panthera_pardus:0.1)98:0.2,Panthera_tigris:0.3);"
    output_tex = tmp_path / "tree.tex"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--newick",
            sample_newick,
            "--output",
            str(output_tex),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, (
        f"newick_to_forest.py failed with code {result.returncode}:\n"
        f"Stderr: {result.stderr}"
    )
    assert output_tex.exists(), "Forest output file not created"

    tex_content = output_tex.read_text(encoding="utf-8")
    assert r"\begin{forest}" in tex_content, "Forest LaTeX environment not opened"
    assert r"\end{forest}" in tex_content, "Forest LaTeX environment not closed"
    assert "Panthera" in tex_content, "Taxon names missing from forest output"


def test_format_table_csv_to_booktabs(project_root, tmp_path):
    """T3-INT-04: format_table.py converts CSV data into booktabs + siunitx LaTeX tables."""
    script_path = (
        project_root
        / ".agents"
        / "skills"
        / "bio-scientific-formatting"
        / "scripts"
        / "format_table.py"
    )
    if not script_path.exists():
        pytest.skip(f"format_table.py not yet implemented at {script_path}")

    sample_csv = tmp_path / "sample_morpho.csv"
    sample_csv.write_text(
        "SpecimenID,Taxon,HeadLength,BodyMass\n"
        "MCZ-101,Panthera leo,245.2,185.4\n"
        "MCZ-102,Panthera pardus,198.6,62.1\n",
        encoding="utf-8",
    )
    output_tex = tmp_path / "table.tex"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--input",
            str(sample_csv),
            "--output",
            str(output_tex),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, (
        f"format_table.py failed with code {result.returncode}:\n"
        f"Stderr: {result.stderr}"
    )
    assert output_tex.exists(), "Table output file not created"

    tex_content = output_tex.read_text(encoding="utf-8")
    for required_macro in [r"\toprule", r"\midrule", r"\bottomrule"]:
        assert required_macro in tex_content, f"Macro '{required_macro}' missing in generated table"


def test_validate_nomenclature_rules(project_root, tmp_path):
    """T3-INT-05: validate_nomenclature.py inspects LaTeX files for ICZN and ethics compliance."""
    script_path = (
        project_root
        / ".agents"
        / "skills"
        / "bio-nomenclature-ethics"
        / "scripts"
        / "validate_nomenclature.py"
    )
    if not script_path.exists():
        pytest.skip(f"validate_nomenclature.py not yet implemented at {script_path}")

    # Valid Life Sciences snippet: italicized binomial, IACUC statement
    valid_tex = tmp_path / "valid_methods.tex"
    valid_tex.write_text(
        r"""\section{Methods}
Specimens of \textit{Panthera leo} were studied under IACUC protocol #2024-0812.
""",
        encoding="utf-8",
    )

    result_valid = subprocess.run(
        [sys.executable, str(script_path), "--file", str(valid_tex)],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result_valid.returncode == 0, f"Validator falsely flagged valid file: {result_valid.stdout}"

    # Invalid snippet: unitalicized binomial name
    invalid_tex = tmp_path / "invalid_methods.tex"
    invalid_tex.write_text(
        r"""\section{Methods}
We observed Panthera leo in the wild without approval.
""",
        encoding="utf-8",
    )

    result_invalid = subprocess.run(
        [sys.executable, str(script_path), "--file", str(invalid_tex)],
        capture_output=True,
        text=True,
        timeout=15,
    )
    # The script should report violations (either non-zero exit code or warning report)
    output = (result_invalid.stdout + result_invalid.stderr).lower()
    assert "panthera leo" in output or "iacuc" in output or result_invalid.returncode != 0, (
        "Validator failed to detect nomenclature or ethics violation"
    )
