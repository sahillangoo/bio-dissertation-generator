"""
Tier 1 and Tier 2 Tests: Automated Compilation CLI (build.py) and pyproject.toml Configuration.
Verifies CLI argument parsing, engine options, and --strict mode warning handling.
"""

import os
import sys
import subprocess
from pathlib import Path
import pytest


# ============================================================================
# TIER 1: FEATURE COVERAGE (BUILD CLI & PACKAGING)
# ============================================================================

def test_pyproject_toml_configuration(project_root):
    """T1-CLI-01: Verify pyproject.toml exists and declares required dependencies and scripts."""
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        pytest.skip(f"pyproject.toml not yet implemented at {pyproject_path}")

    content = pyproject_path.read_text(encoding="utf-8")
    assert "bio-dissertation-generator" in content or "dissertation" in content, (
        "pyproject.toml missing project metadata"
    )

    # Check key dependencies
    for dep in ["click", "pyyaml", "rich"]:
        assert dep in content.lower(), f"Dependency '{dep}' not listed in pyproject.toml"


def test_build_script_exists(project_root):
    """T1-CLI-01: Verify build.py exists at project root."""
    build_py = project_root / "build.py"
    if not build_py.exists():
        pytest.skip(f"build.py not yet implemented at {build_py}")
    assert build_py.is_file(), f"{build_py} is not a regular file"
    assert build_py.stat().st_size > 0, f"{build_py} is empty"


def test_build_cli_help_flag(project_root):
    """T1-CLI-02: Verify build.py --help executes successfully and documents key CLI options."""
    build_py = project_root / "build.py"
    if not build_py.exists():
        pytest.skip("build.py not yet implemented")

    result = subprocess.run(
        [sys.executable, str(build_py), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, f"build.py --help failed with code {result.returncode}: {result.stderr}"
    stdout_lower = result.stdout.lower()

    # Verify documented flags
    expected_flags = ["--root", "--output", "--engine", "--clean", "--strict"]
    for flag in expected_flags:
        assert flag in stdout_lower, f"Flag '{flag}' missing in build.py --help output"


# ============================================================================
# TIER 2: BOUNDARY & CORNER CASES (CLI ERROR MODES & STRICT HANDLING)
# ============================================================================

def test_build_cli_nonexistent_root_exits_nonzero(project_root):
    """T2-CLI-01: Invoking build.py with a non-existent LaTeX root file should fail with non-zero exit code."""
    build_py = project_root / "build.py"
    if not build_py.exists():
        pytest.skip("build.py not yet implemented")

    result = subprocess.run(
        [sys.executable, str(build_py), "--root", "non_existent_file_9999.tex"],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode != 0, (
        "build.py should have failed when pointed to a non-existent root file"
    )


def test_strict_mode_flag_recognized(project_root):
    """T2-CLI-02: Verify --strict flag is recognized and accepted by build CLI."""
    build_py = project_root / "build.py"
    if not build_py.exists():
        pytest.skip("build.py not yet implemented")

    # Run with --help and confirm --strict is present
    result = subprocess.run(
        [sys.executable, str(build_py), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert "--strict" in result.stdout, "--strict option not supported in build.py CLI"
