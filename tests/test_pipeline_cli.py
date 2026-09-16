"""
Tests for Master Dissertation Pipeline CLI (pipeline.py) and Final Output skill.
Verifies CLI execution, stage listing, status reporting, and single-stage execution.
"""

import json
from pathlib import Path
import subprocess
import sys
import pytest


def test_pipeline_script_exists(project_root):
    """Verify pipeline.py exists at project root."""
    pipeline_py = project_root / "pipeline.py"
    assert pipeline_py.exists(), f"pipeline.py not found at {pipeline_py}"
    assert pipeline_py.is_file(), f"{pipeline_py} is not a regular file"
    assert pipeline_py.stat().st_size > 0, f"{pipeline_py} is empty"


def test_final_output_skill_exists(skills_dir):
    """Verify final-output skill folder and files exist."""
    skill_dir = skills_dir / "final-output"
    assert skill_dir.exists()
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "scripts" / "run_pipeline.py").exists()
    assert (skill_dir / "references" / "pipeline_architecture.md").exists()
    assert (skill_dir / "examples" / "pipeline_run_example.md").exists()


def test_pipeline_cli_help_flag(project_root):
    """Verify pipeline.py --help executes successfully."""
    pipeline_py = project_root / "pipeline.py"
    result = subprocess.run(
        [sys.executable, str(pipeline_py), "--help"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, f"pipeline.py --help failed: {result.stderr}"
    assert "--all" in result.stdout
    assert "--stage" in result.stdout
    assert "--list-stages" in result.stdout
    assert "--status" in result.stdout


def test_pipeline_cli_list_stages(project_root):
    """Verify pipeline.py --list-stages lists all 7 stages."""
    pipeline_py = project_root / "pipeline.py"
    result = subprocess.run(
        [sys.executable, str(pipeline_py), "--list-stages"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0
    expected_stages = [
        "staging",
        "biology_logic",
        "chapter_drafting",
        "citation_audit",
        "adversarial_review",
        "de_ai_humanizer",
        "final_build",
    ]
    for stage in expected_stages:
        assert stage in result.stdout, f"Stage {stage} not found in --list-stages output"


def test_pipeline_status_reporting(project_root):
    """Verify pipeline.py --status reads pipeline_state.json."""
    pipeline_py = project_root / "pipeline.py"
    result = subprocess.run(
        [sys.executable, str(pipeline_py), "--status"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, f"pipeline.py --status failed: {result.stderr}"
    assert "Pipeline State:" in result.stdout or "Stages:" in result.stdout


def test_final_output_wrapper_cli(project_root):
    """Verify .agents/skills/final-output/scripts/run_pipeline.py works."""
    script_path = project_root / ".agents" / "skills" / "final-output" / "scripts" / "run_pipeline.py"
    result = subprocess.run(
        [sys.executable, str(script_path), "--list-stages"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0
    assert "adversarial_review" in result.stdout


def test_pipeline_audit_skills_flag(project_root):
    """Verify pipeline.py --audit-skills catalogs core skills plus examiner playbooks."""
    pipeline_py = project_root / "pipeline.py"
    result = subprocess.run(
        [sys.executable, str(pipeline_py), "--audit-skills"],
        capture_output=True,
        text=True,
        timeout=25,
    )
    assert result.returncode == 0, f"pipeline.py --audit-skills failed: {result.stderr}"
    assert "0 duplicates detected" in result.stdout
    assert "Fork 1: Created Skills" in result.stdout
    assert "Fork 2: External Skills" in result.stdout

    json_inventory = project_root / "pipeline_outputs" / "skills_inventory.json"
    assert json_inventory.exists(), "skills_inventory.json was not generated"
    data = json.loads(json_inventory.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["summary"]["total_skills"] == 8
    assert data["summary"]["created_count"] == 8
    assert data["summary"]["external_count"] == 0
    assert data["summary"]["duplicates_detected"] == 0
    names = {s["name"] for s in data["created_skills"]}
    assert "scholar-language-auditor" in names
    assert "dissertation-checker" in names

    md_inventory = project_root / "pipeline_outputs" / "skills_inventory.md"
    assert md_inventory.exists(), "skills_inventory.md was not generated"
    md_text = md_inventory.read_text(encoding="utf-8")
    assert "Fork 1: Created Skills" in md_text
    assert "Fork 2: External Skills" in md_text


def test_pipeline_list_skills_json(project_root):
    """Verify pipeline.py --list-skills --json outputs machine-readable data."""
    pipeline_py = project_root / "pipeline.py"
    result = subprocess.run(
        [sys.executable, str(pipeline_py), "--list-skills", "--json"],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, f"--list-skills --json failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["status"] == "PASS"
    assert data["summary"]["total_skills"] == 8
    assert len(data["created_skills"]) == 8
    assert len(data["external_skills"]) == 0
    assert len(data["duplicates"]) == 0

