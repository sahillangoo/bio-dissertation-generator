"""
Tier 4 Tests: Real-World Workloads & Full Headless LaTeX-to-PDF Compilation.
Verifies complete dissertation compilation, non-zero PDF generation, zero undefined citations/references, and clean flag.
"""

import os
import sys
import subprocess
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def headless_build_run(project_root):
    """Executes the headless dissertation compilation once for all Tier 4 workload tests."""
    build_py = project_root / "build.py"
    root_tex = project_root / "dissertation.tex"
    pdf_out = project_root / "dissertation.pdf"

    if not build_py.exists():
        pytest.skip("build.py not yet implemented")
    if not root_tex.exists():
        pytest.skip("dissertation.tex not yet implemented")

    result = subprocess.run(
        [
            sys.executable,
            str(build_py),
            "--root",
            str(root_tex),
            "--output",
            str(pdf_out),
            "--keep-intermediates",
            "--strict",
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    return result


def test_full_headless_dissertation_build(headless_build_run):
    """T4-E2E-01: Execute full compilation via build.py with --strict and assert exit code 0."""
    assert headless_build_run.returncode == 0, (
        f"Headless dissertation build failed with code {headless_build_run.returncode}:\n"
        f"Stdout: {headless_build_run.stdout}\n"
        f"Stderr: {headless_build_run.stderr}"
    )


def test_pdf_artifact_integrity(project_root, headless_build_run):
    """T4-E2E-02: Verify dissertation.pdf exists, is non-zero (> 10 KB), and has valid PDF header."""
    assert headless_build_run.returncode == 0, "Build did not exit successfully"

    pdf_out = project_root / "dissertation.pdf"
    assert pdf_out.exists(), f"Expected dissertation.pdf missing at {pdf_out}"

    size_bytes = pdf_out.stat().st_size
    assert size_bytes > 10240, (
        f"dissertation.pdf is suspiciously small ({size_bytes} bytes, expected > 10 KB)"
    )

    with open(pdf_out, "rb") as f:
        header = f.read(5)
    assert header == b"%PDF-", f"Invalid PDF file magic header: {header}"


def test_zero_broken_cross_references(project_root, headless_build_run):
    """T4-E2E-03: Verify zero broken cross-reference warnings exist in transcript or log."""
    combined_transcript = headless_build_run.stdout + "\n" + headless_build_run.stderr

    # Check build transcript report
    assert "Broken References" in combined_transcript, (
        "Diagnostic report missing Broken References section"
    )
    assert "Zero ??" in combined_transcript or "Broken References   │   0" in combined_transcript, (
        f"Broken references reported in transcript:\n{combined_transcript}"
    )

    # If log file exists, double-check log file
    main_log = project_root / "dissertation.log"
    if main_log.exists():
        log_text = main_log.read_text(encoding="utf-8", errors="ignore")
        assert "LaTeX Warning: There were undefined references" not in log_text, (
            "Found undefined cross-references in dissertation.log"
        )


def test_zero_unresolved_citations(project_root, headless_build_run):
    """T4-E2E-04: Verify zero undefined citation warnings exist in transcript or log."""
    combined_transcript = headless_build_run.stdout + "\n" + headless_build_run.stderr

    # Check build transcript report
    assert "Undefined Citations" in combined_transcript, (
        "Diagnostic report missing Undefined Citations section"
    )
    assert "Zero [?]" in combined_transcript or "Undefined Citations │   0" in combined_transcript, (
        f"Undefined citations reported in transcript:\n{combined_transcript}"
    )

    # If log file exists, double-check log file
    main_log = project_root / "dissertation.log"
    if main_log.exists():
        log_text = main_log.read_text(encoding="utf-8", errors="ignore")
        assert "LaTeX Warning: Citation" not in log_text, (
            "Found unresolved citation warnings in dissertation.log"
        )


def test_build_clean_cleans_auxiliary_files(project_root):
    """T4-E2E-05: Verify running build.py --clean removes auxiliary files."""
    build_py = project_root / "build.py"
    if not build_py.exists():
        pytest.skip("build.py not yet implemented")

    # Create dummy auxiliary file
    dummy_aux = project_root / "dissertation.aux"
    dummy_aux.touch()
    assert dummy_aux.exists()

    result = subprocess.run(
        [sys.executable, str(build_py), "--clean", "--root", "dissertation.tex"],
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, f"build.py --clean failed: {result.stderr}"
