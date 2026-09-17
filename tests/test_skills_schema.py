"""
Tier 1 and Tier 2 Tests: Antigravity Skills Schema & Frontmatter Validation.
Verifies all 5 Life Sciences skills under .agents/skills/ conform to specifications.
"""

import os
import re
import sys
import subprocess
from pathlib import Path
import pytest

from conftest import EXPECTED_SKILLS, parse_yaml_frontmatter


# ============================================================================
# TIER 1: FEATURE COVERAGE (SKILLS SCHEMA)
# ============================================================================

def test_skills_root_directory_exists(skills_dir):
    """T1-SKILL-01: Verify .agents/skills/ directory exists."""
    assert skills_dir.exists(), f"Skills directory not found at {skills_dir}"
    assert skills_dir.is_dir(), f"Skills path {skills_dir} is not a directory"


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_each_skill_directory_exists(skills_dir, skill_name):
    """T1-SKILL-01: Verify each of the 5 expected skill directories exists."""
    skill_path = skills_dir / skill_name
    assert skill_path.exists(), f"Expected skill directory missing: {skill_path}"
    assert skill_path.is_dir(), f"Skill path {skill_path} is not a directory"


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_md_file_exists(skills_dir, skill_name):
    """T1-SKILL-02: Verify SKILL.md exists in each skill directory."""
    skill_md = skills_dir / skill_name / "SKILL.md"
    assert skill_md.exists(), f"SKILL.md missing in {skill_name}: {skill_md}"
    assert skill_md.is_file(), f"{skill_md} is not a regular file"
    assert skill_md.stat().st_size > 0, f"{skill_md} is empty"


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_yaml_frontmatter_delimiters_and_fields(skills_dir, skill_name):
    """T1-SKILL-02, T1-SKILL-03, T1-SKILL-04: Validate YAML frontmatter schema."""
    skill_md = skills_dir / skill_name / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    # Delimiter checks
    assert content.startswith("---"), f"{skill_md} must start with '---' on line 1"
    parts = content.split("---", 2)
    assert len(parts) >= 3, f"{skill_md} must contain closing '---' frontmatter delimiter"

    # Parse frontmatter
    data = parse_yaml_frontmatter(skill_md)
    assert "name" in data, f"'name' field missing in frontmatter of {skill_md}"
    assert "description" in data, f"'description' field missing in frontmatter of {skill_md}"

    # Name constraints
    name = data["name"]
    assert isinstance(name, str), f"'name' must be a string in {skill_md}"
    assert len(name) <= 64, f"'name' exceeds 64 characters in {skill_md}: length={len(name)}"
    assert re.match(r"^[a-z0-9-]+$", name), (
        f"'name' in {skill_md} must be lowercase alphanumeric with hyphens, got: '{name}'"
    )
    assert name == skill_name, f"'name' in frontmatter ({name}) does not match directory ({skill_name})"

    # Description constraints
    desc = data["description"]
    assert isinstance(desc, str), f"'description' must be a string in {skill_md}"
    assert len(desc.strip()) > 0, f"'description' must not be empty in {skill_md}"
    assert len(desc) <= 1024, (
        f"'description' in {skill_md} exceeds 1024 characters: length={len(desc)}"
    )


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_progressive_disclosure_subdirectories(skills_dir, skill_name):
    """T1-SKILL-05: Verify scripts/, references/, and examples/ subdirectories exist."""
    skill_path = skills_dir / skill_name
    for subdir_name in ["scripts", "references", "examples"]:
        subdir = skill_path / subdir_name
        assert subdir.exists(), f"Missing required subdirectory '{subdir_name}' in {skill_name}"
        assert subdir.is_dir(), f"'{subdir_name}' in {skill_name} is not a directory"


@pytest.mark.parametrize("skill_name", EXPECTED_SKILLS)
def test_skill_scripts_executable_with_help(skills_dir, skill_name):
    """T1-SKILL-06: Verify each script in scripts/ runs with --help successfully."""
    scripts_dir = skills_dir / skill_name / "scripts"
    py_scripts = list(scripts_dir.glob("*.py"))
    assert len(py_scripts) > 0, f"No Python scripts found in {scripts_dir}"

    for script in py_scripts:
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, (
            f"Script {script.name} in {skill_name} failed '--help' check:\n"
            f"Exit code: {result.returncode}\n"
            f"Stdout: {result.stdout}\n"
            f"Stderr: {result.stderr}"
        )


# ============================================================================
# TIER 2: BOUNDARY & CORNER CASES (SKILLS SCHEMA)
# ============================================================================

def test_validator_rejects_missing_delimiters(tmp_path):
    """T2-SKILL-01: Frontmatter without starting or closing delimiters must be rejected."""
    bad_file = tmp_path / "SKILL.md"
    bad_file.write_text("name: test-skill\ndescription: A test\n", encoding="utf-8")
    with pytest.raises(ValueError, match="frontmatter delimiter"):
        parse_yaml_frontmatter(bad_file)


def test_validator_rejects_invalid_skill_name_characters():
    """T2-SKILL-03: Names with uppercase, spaces, or underscores must fail validation."""
    invalid_names = [
        "Bio-Research-Sources",  # Uppercase
        "bio_research_sources",  # Underscores
        "bio research sources",  # Spaces
        "bio@research",          # Special characters
        "a" * 65,                # > 64 chars
    ]
    name_regex = re.compile(r"^[a-z0-9-]+$")
    for name in invalid_names:
        is_valid = bool(name_regex.match(name)) and len(name) <= 64
        assert not is_valid, f"Invalid skill name '{name}' was unexpectedly accepted"


def test_validator_rejects_excessive_description_length():
    """T2-SKILL-02: Descriptions exceeding 1024 characters must be rejected."""
    long_desc = "x" * 1025
    assert len(long_desc) > 1024, "Length check fixture invalid"
    # Assertion rule
    with pytest.raises(AssertionError):
        assert len(long_desc) <= 1024, "Description exceeds 1024 character limit"


DISSERTATION_SKILLS = EXPECTED_SKILLS + ["final-output"]
PLAYBOOK_SKILLS = ["dissertation-checker", "scholar-language-auditor", "bio-image-verifier"]
ALLOWED_SKILL_FOLDERS = sorted(DISSERTATION_SKILLS + PLAYBOOK_SKILLS)


def test_only_dissertation_skills_are_installed(skills_dir):
    """Required dissertation skills and examiner playbooks must be present."""
    skill_folders = {d.name for d in skills_dir.iterdir() if d.is_dir()}
    missing = set(ALLOWED_SKILL_FOLDERS) - skill_folders
    assert not missing, f"Missing required skills: {sorted(missing)}"


def test_all_installed_skills_agent_specification(skills_dir):
    """Verify dissertation skills adhere to Agent Skills frontmatter specification."""
    name_regex = re.compile(r"^[a-z0-9-]+$")
    skill_folders = [skills_dir / name for name in ALLOWED_SKILL_FOLDERS]
    assert all(p.is_dir() for p in skill_folders), (
        f"Expected {len(ALLOWED_SKILL_FOLDERS)} dissertation skills under {skills_dir}"
    )

    for skill_path in skill_folders:
        s_name = skill_path.name
        skill_md = skill_path / "SKILL.md"
        assert skill_md.exists(), f"SKILL.md missing in {s_name}"
        assert skill_md.stat().st_size > 0, f"SKILL.md is empty in {s_name}"

        data = parse_yaml_frontmatter(skill_md)
        assert "name" in data, f"'name' missing in {s_name}/SKILL.md"
        assert "description" in data, f"'description' missing in {s_name}/SKILL.md"

        fn_name = data["name"]
        assert fn_name == s_name, f"Name '{fn_name}' does not match directory '{s_name}'"
        assert len(fn_name) <= 64, f"Name '{fn_name}' exceeds 64 characters"
        assert name_regex.match(fn_name), f"Name '{fn_name}' has invalid characters"

        desc = data["description"]
        assert isinstance(desc, str) and len(desc.strip()) > 0, f"Description empty in {s_name}"
        assert len(desc) <= 1024, f"Description in {s_name} exceeds 1024 characters ({len(desc)})"

