"""
Tests for Automated Verification & Diagnostic Suite (verify.py).
Verifies CLI argument parsing, flags, passes, JSON output, and execution.
"""

import json
from pathlib import Path
import subprocess
import sys
import pytest


def test_verify_script_exists(project_root):
    """Verify verify.py exists at project root."""
    verify_py = project_root / "verify.py"
    assert verify_py.exists(), f"verify.py not found at {verify_py}"
    assert verify_py.is_file(), f"{verify_py} is not a regular file"
    assert verify_py.stat().st_size > 0, f"{verify_py} is empty"


def test_verify_cli_help_flag(project_root):
    """Verify verify.py --help executes successfully and documents required flags."""
    verify_py = project_root / "verify.py"
    result = subprocess.run(
        [sys.executable, str(verify_py), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, f"verify.py --help failed: {result.stderr}"
    stdout_lower = result.stdout.lower()

    required_flags = ["--skills-only", "--staging-only", "--build-only", "--json", "--strict"]
    for flag in required_flags:
        assert flag in stdout_lower, f"Flag '{flag}' missing in verify.py --help output"


def test_verify_skills_only_pass(project_root):
    """Verify verify.py --skills-only executes and passes."""
    verify_py = project_root / "verify.py"
    result = subprocess.run(
        [sys.executable, str(verify_py), "--skills-only"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"verify.py --skills-only failed with code {result.returncode}:\n{result.stdout}\n{result.stderr}"
    assert "Pass 1: Antigravity Skills Schema" in result.stdout
    assert "Overall Status: PASS" in result.stdout


def test_verify_staging_only_pass(project_root):
    """Verify verify.py --staging-only executes and passes."""
    verify_py = project_root / "verify.py"
    result = subprocess.run(
        [sys.executable, str(verify_py), "--staging-only"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"verify.py --staging-only failed with code {result.returncode}:\n{result.stdout}\n{result.stderr}"
    assert "Pass 2: Research Sources Staging" in result.stdout
    assert "Overall Status: PASS" in result.stdout


def test_verify_json_output_mode(project_root):
    """Verify verify.py --staging-only --json outputs valid JSON structure."""
    verify_py = project_root / "verify.py"
    result = subprocess.run(
        [sys.executable, str(verify_py), "--staging-only", "--json"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"verify.py --json failed: {result.stderr}"

    data = json.loads(result.stdout)
    assert data["suite"] == "bio-dissertation-generator-verification"
    assert data["overall_status"] == "PASS"
    assert "summary" in data
    assert data["summary"]["failed"] == 0
    assert "passes" in data
    assert len(data["passes"]) == 1
    assert data["passes"][0]["pass_id"] == "staging"
