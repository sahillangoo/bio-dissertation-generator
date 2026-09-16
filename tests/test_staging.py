"""
Tier 1 and Tier 2 Tests: Research Staging Architecture & Ingestion Robustness.
Verifies research_sources/ directory hierarchy, documentation, and boundary conditions.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import pytest

from conftest import EXPECTED_STAGING_DIRS


# ============================================================================
# TIER 1: FEATURE COVERAGE (STAGING ARCHITECTURE)
# ============================================================================

def test_staging_root_directory_exists(staging_dir):
    """T1-STAGE-01: Verify research_sources/ exists."""
    assert staging_dir.exists(), f"Staging directory missing: {staging_dir}"
    assert staging_dir.is_dir(), f"Staging path {staging_dir} is not a directory"


@pytest.mark.parametrize("subdir_name", EXPECTED_STAGING_DIRS)
def test_all_staging_subdirectories_exist(staging_dir, subdir_name):
    """T1-STAGE-01: Verify existing_work/, papers/, citations/, and notes/ exist."""
    subdir = staging_dir / subdir_name
    assert subdir.exists(), f"Expected staging subdirectory missing: {subdir}"
    assert subdir.is_dir(), f"{subdir} is not a directory"


@pytest.mark.parametrize("subdir_name", EXPECTED_STAGING_DIRS)
def test_staging_subdirectories_contain_gitkeep(staging_dir, subdir_name):
    """T1-STAGE-03: Verify .gitkeep is preserved in each staging subdirectory."""
    gitkeep = staging_dir / subdir_name / ".gitkeep"
    assert gitkeep.exists(), f".gitkeep missing in {subdir_name}: {gitkeep}"


def test_staging_readme_exists_and_contains_instructions(staging_dir):
    """T1-STAGE-02: Verify README.md exists and provides clear student onboarding."""
    readme_path = staging_dir / "README.md"
    assert readme_path.exists(), f"README.md missing in {staging_dir}"
    assert readme_path.is_file(), f"{readme_path} is not a regular file"
    assert readme_path.stat().st_size > 100, f"{readme_path} is too short (< 100 bytes)"

    content = readme_path.read_text(encoding="utf-8").lower()
    for expected_keyword in ["existing_work", "papers", "citations", "notes"]:
        assert expected_keyword in content, (
            f"Expected keyword '{expected_keyword}' missing in staging README.md"
        )


def test_staging_sample_life_sciences_files_exist(staging_dir):
    """T1-STAGE-04: Verify realistic life sciences sample files exist in staging."""
    existing_work_files = list((staging_dir / "existing_work").glob("*.*"))
    # Filter out .gitkeep
    sample_files = [f for f in existing_work_files if f.name != ".gitkeep"]
    assert len(sample_files) > 0, "No sample files staged in research_sources/existing_work/"

    # Check for presence of methods draft or morphometric table
    sample_names = [f.name for f in sample_files]
    assert any(name.endswith((".md", ".txt", ".tex")) for name in sample_names), (
        f"No draft document found in existing_work/: {sample_names}"
    )


# ============================================================================
# TIER 2: BOUNDARY & CORNER CASES (STAGING INGESTION)
# ============================================================================

def test_empty_staging_directory_ingestion_resilience(tmp_path, project_root):
    """T2-STAGE-01: Ingesting an empty staging directory should succeed gracefully."""
    ingest_script = (
        project_root
        / ".agents"
        / "skills"
        / "bio-research-sources"
        / "scripts"
        / "ingest_sources.py"
    )
    if not ingest_script.exists():
        pytest.skip(f"ingest_sources.py not yet implemented at {ingest_script}")

    # Create empty staging structure with only .gitkeep
    empty_sources = tmp_path / "empty_sources"
    for d in EXPECTED_STAGING_DIRS:
        subdir = empty_sources / d
        subdir.mkdir(parents=True, exist_ok=True)
        (subdir / ".gitkeep").touch()

    output_manifest = tmp_path / "sources_manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ingest_script),
            "--sources",
            str(empty_sources),
            "--output",
            str(output_manifest),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, (
        f"ingest_sources.py crashed on empty staging directory:\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )
    assert output_manifest.exists(), "Manifest file was not generated"

    manifest_data = json.loads(output_manifest.read_text(encoding="utf-8"))
    assert isinstance(manifest_data, (list, dict)), "Manifest must be a JSON array or dict"
    if isinstance(manifest_data, list):
        assert len(manifest_data) == 0, "Manifest should be empty when no staged files exist"
    elif isinstance(manifest_data, dict):
        assert len(manifest_data.get("files", [])) == 0, (
            "Manifest files list should be empty when no staged files exist"
        )


def test_unsupported_file_extension_handling(tmp_path, project_root):
    """T2-STAGE-02: Staging unhandled or binary extensions should not crash the ingest script."""
    ingest_script = (
        project_root
        / ".agents"
        / "skills"
        / "bio-research-sources"
        / "scripts"
        / "ingest_sources.py"
    )
    if not ingest_script.exists():
        pytest.skip(f"ingest_sources.py not yet implemented at {ingest_script}")

    test_sources = tmp_path / "test_sources"
    existing_work = test_sources / "existing_work"
    existing_work.mkdir(parents=True, exist_ok=True)
    # Write a binary file
    (existing_work / "unknown_raw_data.bin").write_bytes(b"\x00\x01\x02\x03\xff\xfe")

    output_manifest = tmp_path / "manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ingest_script),
            "--sources",
            str(test_sources),
            "--output",
            str(output_manifest),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, (
        f"ingest_sources.py crashed on unhandled binary extension:\n"
        f"Stderr: {result.stderr}"
    )
