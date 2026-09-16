#!/usr/bin/env python3
"""
verify.py - Automated Diagnostic & Verification Suite for Biology & Zoology Dissertation Suite.

Executes comprehensive three-pass validation:
  Pass 1: Antigravity Skills Schema & Progressive Disclosure Validation (.agents/skills/)
  Pass 2: Research Sources Staging & Automated Ingestion Integration (research_sources/)
  Pass 3: Headless End-to-End LaTeX Compilation & Cross-Reference Diagnostic Integrity

Exit codes:
  0: All executed diagnostic passes passed with 100% success.
  1: One or more diagnostic checks failed (or warnings in --strict mode).
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from typing import Any, Dict, List, Optional, Set, Tuple

# Attempt Rich and Click imports; provide graceful plain-text fallbacks
try:
    import click
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None

# Attempt PyYAML; provide pure-python fallback parser
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


EXPECTED_SKILLS = [
    "bio-research-sources",
    "bio-nomenclature-ethics",
    "bio-chapter-builder",
    "bio-reference-manager",
    "bio-scientific-formatting",
]

EXPECTED_STAGING_DIRS = [
    "existing_work",
    "papers",
    "citations",
    "notes",
]

EXPECTED_FRONTMATTER_FILES = [
    "title.tex",
    "abstract.tex",
    "dedication.tex",
    "acknowledgements.tex",
    "abbreviations.tex",
    "ethics_statement.tex",
]

EXPECTED_CHAPTER_FILES = [
    "01_introduction.tex",
    "02_lit_review.tex",
    "03_methods.tex",
    "04_results.tex",
    "05_discussion.tex",
]

EXPECTED_APPENDIX_FILES = [
    "appendix_a_specimens.tex",
    "appendix_b_primers.tex",
    "appendix_c_stats.tex",
]


@dataclass
class CheckResult:
    """Individual verification check outcome."""
    name: str
    status: str  # "PASS", "FAIL", "WARN", "SKIP"
    message: str
    details: List[str] = field(default_factory=list)
    duration_ms: float = 0.0


@dataclass
class PassResult:
    """Outcome for an entire diagnostic pass."""
    pass_id: str
    title: str
    status: str  # "PASS", "FAIL", "WARN"
    checks: List[CheckResult] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def passed_count(self) -> int:
        return sum(1 for c in self.checks if c.status == "PASS")

    @property
    def failed_count(self) -> int:
        return sum(1 for c in self.checks if c.status == "FAIL")

    @property
    def warned_count(self) -> int:
        return sum(1 for c in self.checks if c.status == "WARN")


def parse_yaml_frontmatter(file_path: Path) -> Dict[str, Any]:
    """Parse YAML frontmatter delimited by '---' from a markdown file."""
    text = file_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"File {file_path.name} does not start with frontmatter delimiter '---'")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"File {file_path.name} does not have a closing '---' frontmatter delimiter")

    frontmatter_raw = parts[1].strip()

    if HAS_YAML:
        data = yaml.safe_load(frontmatter_raw)
        if isinstance(data, dict):
            return data

    # Pure-Python robust fallback parser
    data: Dict[str, Any] = {}
    lines = frontmatter_raw.splitlines()
    current_key = None
    multiline_val: List[str] = []
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


def extract_bibtex_keys(bib_path: Path) -> Set[str]:
    """Extract entry citation keys from a .bib file."""
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    keys = re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", text)
    return set(keys)


def extract_latex_citations(file_path: Path) -> Set[str]:
    """Extract cited keys in LaTeX files using citation macros."""
    if not file_path.exists():
        return set()
    text = file_path.read_text(encoding="utf-8", errors="replace")
    raw_citations = re.findall(
        r"\\(?:cite|parencite|textcite|citep|citet|autocite)(?:\[[^\]]*\])*\{([^}]+)\}",
        text
    )
    cited_keys: Set[str] = set()
    for citation_group in raw_citations:
        for key in citation_group.split(","):
            cleaned = key.strip()
            if cleaned:
                cited_keys.add(cleaned)
    return cited_keys


# ============================================================================
# DIAGNOSTIC PASS 1: SKILLS SCHEMA & PROGRESSIVE DISCLOSURE
# ============================================================================

def verify_skills(project_root: Path, strict: bool = False, verbose: bool = False) -> PassResult:
    """Validate all Antigravity skill folders under .agents/skills/."""
    start_time = time.perf_counter()
    pass_res = PassResult(
        pass_id="skills",
        title="Pass 1: Antigravity Skills Schema & Progressive Disclosure",
        status="PASS"
    )

    skills_dir = project_root / ".agents" / "skills"
    if not skills_dir.exists() or not skills_dir.is_dir():
        pass_res.checks.append(CheckResult(
            name="Skills Root Directory",
            status="FAIL",
            message=f"Skills directory not found at {skills_dir}"
        ))
        pass_res.status = "FAIL"
        pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
        return pass_res

    pass_res.checks.append(CheckResult(
        name="Skills Root Directory",
        status="PASS",
        message=f"Found skills directory at {skills_dir.relative_to(project_root)}"
    ))

    # Discover skill subdirectories
    skill_folders = [d for d in skills_dir.iterdir() if d.is_dir()]
    skill_names = {d.name for d in skill_folders}

    # Verify expected skills are present
    missing_expected = set(EXPECTED_SKILLS) - skill_names
    if missing_expected:
        pass_res.checks.append(CheckResult(
            name="Expected Skills Inventory",
            status="FAIL",
            message=f"Missing expected skill directories: {', '.join(sorted(missing_expected))}"
        ))
        pass_res.status = "FAIL"
    else:
        pass_res.checks.append(CheckResult(
            name="Expected Skills Inventory",
            status="PASS",
            message=f"All {len(EXPECTED_SKILLS)} expected skill suites present ({', '.join(EXPECTED_SKILLS)})"
        ))

    # Validate each skill suite
    name_regex = re.compile(r"^[a-z0-9-]+$")

    for skill_path in sorted(skill_folders):
        s_name = skill_path.name
        t0 = time.perf_counter()
        skill_details: List[str] = []
        skill_failed = False
        skill_warned = False

        # 1. SKILL.md existence
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists() or not skill_md.is_file():
            pass_res.checks.append(CheckResult(
                name=f"Skill File: {s_name}/SKILL.md",
                status="FAIL",
                message=f"SKILL.md missing in {s_name}",
                duration_ms=(time.perf_counter() - t0) * 1000
            ))
            pass_res.status = "FAIL"
            continue

        # 2. YAML frontmatter validation
        try:
            frontmatter = parse_yaml_frontmatter(skill_md)
        except Exception as err:
            pass_res.checks.append(CheckResult(
                name=f"Frontmatter Delimiters: {s_name}",
                status="FAIL",
                message=f"Frontmatter parsing failed in {s_name}: {err}",
                duration_ms=(time.perf_counter() - t0) * 1000
            ))
            pass_res.status = "FAIL"
            continue

        # Validate name
        fn_name = frontmatter.get("name")
        if not fn_name or not isinstance(fn_name, str):
            skill_failed = True
            skill_details.append("Missing or non-string 'name' in frontmatter")
        elif len(fn_name) > 64:
            skill_failed = True
            skill_details.append(f"'name' exceeds 64 characters ({len(fn_name)} chars)")
        elif not name_regex.match(fn_name):
            skill_failed = True
            skill_details.append(f"'name' contains invalid characters (must match ^[a-z0-9-]+$): '{fn_name}'")
        elif fn_name != s_name:
            skill_failed = True
            skill_details.append(f"'name' ({fn_name}) does not match folder name ({s_name})")

        # Validate description
        desc = frontmatter.get("description")
        if not desc or not isinstance(desc, str) or not desc.strip():
            skill_failed = True
            skill_details.append("Missing or empty 'description' in frontmatter")
        elif len(desc) > 1024:
            skill_failed = True
            skill_details.append(f"'description' exceeds 1024 characters ({len(desc)} chars)")

        # 3. Progressive disclosure directories
        for req_subdir in ["scripts", "references", "examples"]:
            target_sub = skill_path / req_subdir
            if not target_sub.exists() or not target_sub.is_dir():
                skill_failed = True
                skill_details.append(f"Missing required progressive disclosure directory: '{req_subdir}/'")

        # 4. CLI Scripts execution check
        scripts_dir = skill_path / "scripts"
        if scripts_dir.exists() and scripts_dir.is_dir():
            py_scripts = list(scripts_dir.glob("*.py"))
            if not py_scripts:
                if strict:
                    skill_failed = True
                    skill_details.append(f"No Python scripts found in {s_name}/scripts/")
                else:
                    skill_warned = True
                    skill_details.append(f"No Python scripts in {s_name}/scripts/ (warning)")
            for script in py_scripts:
                try:
                    res = subprocess.run(
                        [sys.executable, str(script), "--help"],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if res.returncode != 0:
                        skill_failed = True
                        skill_details.append(f"Script {script.name} --help exited with code {res.returncode}")
                except Exception as ex:
                    skill_failed = True
                    skill_details.append(f"Script {script.name} --help execution error: {ex}")

        # Check status outcome
        if skill_failed:
            status = "FAIL"
            pass_res.status = "FAIL"
            msg = f"Skill schema validation failed for {s_name}"
        elif skill_warned:
            status = "WARN" if not strict else "FAIL"
            if strict:
                pass_res.status = "FAIL"
            msg = f"Skill {s_name} passed with warnings"
        else:
            status = "PASS"
            msg = f"Skill {s_name} verified (name, description, scripts, references, examples)"

        pass_res.checks.append(CheckResult(
            name=f"Skill Suite: {s_name}",
            status=status,
            message=msg,
            details=skill_details,
            duration_ms=(time.perf_counter() - t0) * 1000
        ))

    pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
    return pass_res


# ============================================================================
# DIAGNOSTIC PASS 2: RESEARCH STAGING & INGESTION INTEGRATION
# ============================================================================

def verify_staging(project_root: Path, strict: bool = False, verbose: bool = False) -> PassResult:
    """Validate research_sources/ hierarchy, onboarding guide, and manifest generator."""
    start_time = time.perf_counter()
    pass_res = PassResult(
        pass_id="staging",
        title="Pass 2: Research Sources Staging & Ingestion Integration",
        status="PASS"
    )

    staging_dir = project_root / "research_sources"
    if not staging_dir.exists() or not staging_dir.is_dir():
        pass_res.checks.append(CheckResult(
            name="Staging Root Directory",
            status="FAIL",
            message=f"Research staging directory missing at {staging_dir}"
        ))
        pass_res.status = "FAIL"
        pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
        return pass_res

    pass_res.checks.append(CheckResult(
        name="Staging Root Directory",
        status="PASS",
        message="Staging root directory 'research_sources/' exists"
    ))

    # 1. Subdirectory and .gitkeep checks
    subdirs_ok = True
    missing_subdirs = []
    missing_gitkeeps = []

    for sub in EXPECTED_STAGING_DIRS:
        subdir_path = staging_dir / sub
        if not subdir_path.exists() or not subdir_path.is_dir():
            subdirs_ok = False
            missing_subdirs.append(sub)
        else:
            gitkeep = subdir_path / ".gitkeep"
            if not gitkeep.exists():
                missing_gitkeeps.append(sub)

    if missing_subdirs:
        pass_res.checks.append(CheckResult(
            name="Staging Subdirectory Hierarchy",
            status="FAIL",
            message=f"Missing staging subdirectories: {', '.join(missing_subdirs)}"
        ))
        pass_res.status = "FAIL"
    else:
        pass_res.checks.append(CheckResult(
            name="Staging Subdirectory Hierarchy",
            status="PASS",
            message=f"All 4 staging subdirectories present ({', '.join(EXPECTED_STAGING_DIRS)})"
        ))

    if missing_gitkeeps:
        status = "WARN" if not strict else "FAIL"
        if strict:
            pass_res.status = "FAIL"
        pass_res.checks.append(CheckResult(
            name="Staging .gitkeep Preservation",
            status=status,
            message=f".gitkeep missing in: {', '.join(missing_gitkeeps)}"
        ))
    else:
        pass_res.checks.append(CheckResult(
            name="Staging .gitkeep Preservation",
            status="PASS",
            message="All staging subdirectories contain preserved .gitkeep files"
        ))

    # 2. Onboarding Documentation README.md
    readme_path = staging_dir / "README.md"
    if not readme_path.exists() or not readme_path.is_file():
        pass_res.checks.append(CheckResult(
            name="Staging Onboarding Documentation",
            status="FAIL",
            message="research_sources/README.md does not exist"
        ))
        pass_res.status = "FAIL"
    else:
        content = readme_path.read_text(encoding="utf-8", errors="replace").lower()
        size = readme_path.stat().st_size
        missing_kw = [kw for kw in EXPECTED_STAGING_DIRS if kw not in content]
        if size < 100:
            pass_res.checks.append(CheckResult(
                name="Staging Onboarding Documentation",
                status="FAIL",
                message=f"research_sources/README.md is too short ({size} bytes, expected > 100)"
            ))
            pass_res.status = "FAIL"
        elif missing_kw:
            pass_res.checks.append(CheckResult(
                name="Staging Onboarding Documentation",
                status="FAIL",
                message=f"README.md missing staging instructions for: {', '.join(missing_kw)}"
            ))
            pass_res.status = "FAIL"
        else:
            pass_res.checks.append(CheckResult(
                name="Staging Onboarding Documentation",
                status="PASS",
                message=f"README.md verified ({size} bytes, covers all staging workflows)"
            ))

    # 3. Sample Life Sciences Staged Files
    sample_files: List[Path] = []
    for sub in EXPECTED_STAGING_DIRS:
        for f in (staging_dir / sub).glob("*.*"):
            if f.name != ".gitkeep":
                sample_files.append(f)

    if not sample_files:
        status = "WARN" if not strict else "FAIL"
        if strict:
            pass_res.status = "FAIL"
        pass_res.checks.append(CheckResult(
            name="Sample Research Sources",
            status=status,
            message="No sample student draft or data files found in research_sources/"
        ))
    else:
        pass_res.checks.append(CheckResult(
            name="Sample Research Sources",
            status="PASS",
            message=f"Found {len(sample_files)} realistic staged sample files ({', '.join(f.name for f in sample_files[:3])}...)"
        ))

    # 4. Automated Ingestion Script Pipeline Integration
    ingest_script = (
        project_root / ".agents" / "skills" / "bio-research-sources" / "scripts" / "ingest_sources.py"
    )
    if not ingest_script.exists():
        pass_res.checks.append(CheckResult(
            name="Automated Ingestion Pipeline",
            status="FAIL",
            message=f"ingest_sources.py script missing at {ingest_script}"
        ))
        pass_res.status = "FAIL"
    else:
        manifest_out = staging_dir / "sources_manifest.json"
        t0 = time.perf_counter()
        try:
            res = subprocess.run(
                [
                    sys.executable,
                    str(ingest_script),
                    "--sources", str(staging_dir),
                    "--output", str(manifest_out),
                    "--summary"
                ],
                capture_output=True,
                text=True,
                timeout=20
            )
            if res.returncode != 0:
                pass_res.checks.append(CheckResult(
                    name="Automated Ingestion Pipeline",
                    status="FAIL",
                    message=f"ingest_sources.py failed with code {res.returncode}: {res.stderr.strip()}",
                    duration_ms=(time.perf_counter() - t0) * 1000
                ))
                pass_res.status = "FAIL"
            elif not manifest_out.exists():
                pass_res.checks.append(CheckResult(
                    name="Automated Ingestion Pipeline",
                    status="FAIL",
                    message="sources_manifest.json was not created by ingest_sources.py",
                    duration_ms=(time.perf_counter() - t0) * 1000
                ))
                pass_res.status = "FAIL"
            else:
                raw_json = manifest_out.read_text(encoding="utf-8")
                data = json.loads(raw_json)
                indexed_count = len(data.get("files", [])) if isinstance(data, dict) else len(data)
                pass_res.checks.append(CheckResult(
                    name="Automated Ingestion Pipeline",
                    status="PASS",
                    message=f"Manifest successfully generated with {indexed_count} indexed items -> sources_manifest.json",
                    duration_ms=(time.perf_counter() - t0) * 1000
                ))
        except Exception as exc:
            pass_res.checks.append(CheckResult(
                name="Automated Ingestion Pipeline",
                status="FAIL",
                message=f"Execution error invoking ingest_sources.py: {exc}",
                duration_ms=(time.perf_counter() - t0) * 1000
            ))
            pass_res.status = "FAIL"

    pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
    return pass_res


# ============================================================================
# DIAGNOSTIC PASS 3: END-TO-END HEADLESS PDF COMPILATION & INTEGRITY
# ============================================================================

def verify_build(
    project_root: Path,
    root_file: Path,
    output_file: Path,
    engine: str = "auto",
    strict: bool = False,
    verbose: bool = False
) -> PassResult:
    """Execute complete headless compilation and assert zero broken citations/refs."""
    start_time = time.perf_counter()
    pass_res = PassResult(
        pass_id="build",
        title="Pass 3: Headless PDF Compilation & Cross-Reference Integrity",
        status="PASS"
    )

    # 1. Structural prerequisites
    root_tex = project_root / root_file if not root_file.is_absolute() else root_file
    if not root_tex.exists():
        pass_res.checks.append(CheckResult(
            name="Root LaTeX Document",
            status="FAIL",
            message=f"Root document not found at {root_tex}"
        ))
        pass_res.status = "FAIL"
        pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
        return pass_res

    pass_res.checks.append(CheckResult(
        name="Root LaTeX Document",
        status="PASS",
        message=f"Root document exists: {root_tex.name}"
    ))

    # 2. Check modular dependencies
    missing_modular: List[str] = []
    # Frontmatter
    for f in EXPECTED_FRONTMATTER_FILES:
        if not (project_root / "frontmatter" / f).exists():
            missing_modular.append(f"frontmatter/{f}")
    # Chapters
    for c in EXPECTED_CHAPTER_FILES:
        if not (project_root / "chapters" / c).exists():
            missing_modular.append(f"chapters/{c}")
    # Appendices
    for a in EXPECTED_APPENDIX_FILES:
        if not (project_root / "appendices" / a).exists():
            missing_modular.append(f"appendices/{a}")
    # Preamble & Bibliography
    if not (project_root / "preamble.tex").exists():
        missing_modular.append("preamble.tex")
    if not (project_root / "references.bib").exists():
        missing_modular.append("references.bib")

    if missing_modular:
        pass_res.checks.append(CheckResult(
            name="Modular Document Components",
            status="FAIL",
            message=f"Missing modular dependencies: {', '.join(missing_modular)}"
        ))
        pass_res.status = "FAIL"
    else:
        pass_res.checks.append(CheckResult(
            name="Modular Document Components",
            status="PASS",
            message="All frontmatter, chapters, appendices, preamble, and references.bib verified"
        ))

    # 3. Citation integrity audit in source files
    bib_path = project_root / "references.bib"
    defined_keys = extract_bibtex_keys(bib_path)
    all_cited_keys: Set[str] = set()

    for tex_file in project_root.rglob("*.tex"):
        if ".agents" in tex_file.parts or ".venv" in tex_file.parts or "tests" in tex_file.parts:
            continue
        all_cited_keys.update(extract_latex_citations(tex_file))

    unresolved_keys = all_cited_keys - defined_keys
    if unresolved_keys:
        pass_res.checks.append(CheckResult(
            name="Pre-Build Citation Integrity",
            status="FAIL",
            message=f"{len(unresolved_keys)} citation keys missing from references.bib: {', '.join(sorted(unresolved_keys))}"
        ))
        pass_res.status = "FAIL"
    else:
        pass_res.checks.append(CheckResult(
            name="Pre-Build Citation Integrity",
            status="PASS",
            message=f"All {len(all_cited_keys)} cited keys resolved in master references.bib ({len(defined_keys)} total entries)"
        ))

    # 4. Headless Compilation Execution via build.py
    build_py = project_root / "build.py"
    if not build_py.exists():
        pass_res.checks.append(CheckResult(
            name="Build Engine Script",
            status="FAIL",
            message=f"build.py compiler CLI script missing at {build_py}"
        ))
        pass_res.status = "FAIL"
        pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
        return pass_res

    pdf_target = project_root / output_file if not output_file.is_absolute() else output_file
    t_compile = time.perf_counter()

    cmd = [
        sys.executable,
        str(build_py),
        "--root", str(root_tex),
        "--output", str(pdf_target),
        "--engine", engine,
        "--keep-intermediates",
        "--strict",
    ]
    if verbose:
        cmd.append("--verbose")

    try:
        build_proc = subprocess.run(
            cmd,
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=180
        )
        compile_duration_ms = (time.perf_counter() - t_compile) * 1000
        combined_output = build_proc.stdout + "\n" + build_proc.stderr

        if build_proc.returncode != 0:
            pass_res.checks.append(CheckResult(
                name="Headless Compilation Execution",
                status="FAIL",
                message=f"build.py exited with error code {build_proc.returncode}",
                details=[line for line in combined_output.splitlines() if "error" in line.lower() or "fatal" in line.lower()][:8],
                duration_ms=compile_duration_ms
            ))
            pass_res.status = "FAIL"
        else:
            pass_res.checks.append(CheckResult(
                name="Headless Compilation Execution",
                status="PASS",
                message=f"Dissertation compiled successfully (exit code 0, duration {compile_duration_ms/1000:.2f}s)",
                duration_ms=compile_duration_ms
            ))

        # 5. Output PDF Validation
        if not pdf_target.exists():
            pass_res.checks.append(CheckResult(
                name="Output PDF Artifact",
                status="FAIL",
                message=f"Target PDF file was not generated: {pdf_target}"
            ))
            pass_res.status = "FAIL"
        else:
            pdf_size = pdf_target.stat().st_size
            if pdf_size < 10240:
                pass_res.checks.append(CheckResult(
                    name="Output PDF Artifact",
                    status="FAIL",
                    message=f"Generated PDF is suspiciously small ({pdf_size} bytes, expected > 10 KB)"
                ))
                pass_res.status = "FAIL"
            else:
                with open(pdf_target, "rb") as pf:
                    magic = pf.read(5)
                if magic != b"%PDF-":
                    pass_res.checks.append(CheckResult(
                        name="Output PDF Artifact",
                        status="FAIL",
                        message=f"Invalid PDF magic header: {magic}"
                    ))
                    pass_res.status = "FAIL"
                else:
                    pass_res.checks.append(CheckResult(
                        name="Output PDF Artifact",
                        status="PASS",
                        message=f"Valid PDF artifact generated: {pdf_target.name} ({pdf_size / 1024:.2f} KB, magic header %PDF-)"
                    ))

        # 6. Cross-reference and citation diagnostics
        log_file = project_root / f"{root_tex.stem}.log"
        log_content = ""
        if log_file.exists():
            log_content = log_file.read_text(encoding="utf-8", errors="replace")

        # Citations check
        has_broken_cite = (
            "LaTeX Warning: Citation" in log_content
            or ("Undefined Citations" in combined_output and "Zero [?]" not in combined_output and "Undefined Citations │   0" not in combined_output)
        )
        if has_broken_cite:
            pass_res.checks.append(CheckResult(
                name="Zero Undefined Citations Assertion",
                status="FAIL",
                message="Undefined citation warnings ([?]) detected in build log or transcript"
            ))
            pass_res.status = "FAIL"
        else:
            pass_res.checks.append(CheckResult(
                name="Zero Undefined Citations Assertion",
                status="PASS",
                message="100% resolved citations: Zero [?] warnings in output"
            ))

        # Cross-references check
        has_broken_ref = (
            "LaTeX Warning: There were undefined references" in log_content
            or "LaTeX Warning: Reference" in log_content
            or ("Broken References" in combined_output and "Zero ??" not in combined_output and "Broken References   │   0" not in combined_output)
        )
        if has_broken_ref:
            pass_res.checks.append(CheckResult(
                name="Zero Broken Cross-References Assertion",
                status="FAIL",
                message="Broken cross-reference warnings (??) detected in build log or transcript"
            ))
            pass_res.status = "FAIL"
        else:
            pass_res.checks.append(CheckResult(
                name="Zero Broken Cross-References Assertion",
                status="PASS",
                message="100% resolved cross-references: Zero ?? warnings in output"
            ))

    except subprocess.TimeoutExpired:
        pass_res.checks.append(CheckResult(
            name="Headless Compilation Execution",
            status="FAIL",
            message="Compilation timed out after 180 seconds"
        ))
        pass_res.status = "FAIL"
    except Exception as ex:
        pass_res.checks.append(CheckResult(
            name="Headless Compilation Execution",
            status="FAIL",
            message=f"Error executing build.py: {ex}"
        ))
        pass_res.status = "FAIL"

    pass_res.duration_ms = (time.perf_counter() - start_time) * 1000
    return pass_res


# ============================================================================
# CONSOLE FORMATTING & REPORTING
# ============================================================================

def render_rich_report(pass_results: List[PassResult], total_duration_ms: float) -> None:
    """Render structured terminal report with Rich tables and panels."""
    if not console:
        return

    console.print()
    console.print(Panel.fit(
        "[bold cyan]Biology & Zoology Dissertation Suite[/bold cyan]\n"
        "[bold white]Automated System Verification & Diagnostic Suite[/bold white]",
        border_style="cyan"
    ))

    total_checks = sum(len(p.checks) for p in pass_results)
    total_passed = sum(p.passed_count for p in pass_results)
    total_failed = sum(p.failed_count for p in pass_results)
    total_warned = sum(p.warned_count for p in pass_results)

    for p in pass_results:
        table = Table(title=f"\n{p.title} ({p.duration_ms/1000:.2f}s)", show_header=True, expand=True)
        table.add_column("Diagnostic Check", style="bold", ratio=4)
        table.add_column("Status", justify="center", ratio=1)
        table.add_column("Details", ratio=7)

        for c in p.checks:
            if c.status == "PASS":
                status_str = "[bold green]PASS[/bold green]"
            elif c.status == "FAIL":
                status_str = "[bold red]FAIL[/bold red]"
            elif c.status == "WARN":
                status_str = "[bold yellow]WARN[/bold yellow]"
            else:
                status_str = "[dim]SKIP[/dim]"

            details_text = c.message
            if c.details:
                details_text += "\n" + "\n".join(f"  • {d}" for d in c.details)

            table.add_row(c.name, status_str, details_text)

        console.print(table)

    # Overall Summary
    overall_status = "FAIL" if any(p.status == "FAIL" for p in pass_results) else "PASS"
    summary_color = "green" if overall_status == "PASS" else "red"

    summary_text = (
        f"[{summary_color}]Overall Status: {overall_status}[/{summary_color}]\n"
        f"Total Checks: {total_checks} | "
        f"[green]Passed: {total_passed}[/green] | "
        f"[red]Failed: {total_failed}[/red] | "
        f"[yellow]Warnings: {total_warned}[/yellow] | "
        f"Total Elapsed Time: {total_duration_ms/1000:.2f}s"
    )

    console.print()
    console.print(Panel(
        summary_text,
        title="[bold]Verification Summary[/bold]",
        border_style=summary_color
    ))
    console.print()


def render_plain_report(pass_results: List[PassResult], total_duration_ms: float) -> None:
    """Render fallback ASCII text report when Rich is unavailable."""
    print("=" * 80)
    print("Biology & Zoology Dissertation Suite - Automated Diagnostic Suite")
    print("=" * 80)

    total_checks = sum(len(p.checks) for p in pass_results)
    total_passed = sum(p.passed_count for p in pass_results)
    total_failed = sum(p.failed_count for p in pass_results)
    total_warned = sum(p.warned_count for p in pass_results)

    for p in pass_results:
        print(f"\n--- {p.title} ({p.duration_ms/1000:.2f}s) ---")
        for c in p.checks:
            print(f"[{c.status:4}] {c.name}: {c.message}")
            for d in c.details:
                print(f"       • {d}")

    overall_status = "FAIL" if any(p.status == "FAIL" for p in pass_results) else "PASS"
    print("\n" + "=" * 80)
    print(f"Overall Status: {overall_status}")
    print(f"Total Checks: {total_checks} | Passed: {total_passed} | Failed: {total_failed} | Warned: {total_warned}")
    print(f"Elapsed Time: {total_duration_ms/1000:.2f}s")
    print("=" * 80 + "\n")


def build_json_report(pass_results: List[PassResult], total_duration_ms: float) -> Dict[str, Any]:
    """Construct structured dictionary for JSON export."""
    total_checks = sum(len(p.checks) for p in pass_results)
    total_passed = sum(p.passed_count for p in pass_results)
    total_failed = sum(p.failed_count for p in pass_results)
    total_warned = sum(p.warned_count for p in pass_results)
    overall_status = "FAIL" if any(p.status == "FAIL" for p in pass_results) else "PASS"

    return {
        "suite": "bio-dissertation-generator-verification",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "overall_status": overall_status,
        "summary": {
            "total_checks": total_checks,
            "passed": total_passed,
            "failed": total_failed,
            "warned": total_warned,
            "duration_seconds": round(total_duration_ms / 1000, 3),
        },
        "passes": [
            {
                "pass_id": p.pass_id,
                "title": p.title,
                "status": p.status,
                "duration_ms": round(p.duration_ms, 2),
                "checks": [
                    {
                        "name": c.name,
                        "status": c.status,
                        "message": c.message,
                        "details": c.details,
                        "duration_ms": round(c.duration_ms, 2),
                    }
                    for c in p.checks
                ]
            }
            for p in pass_results
        ]
    }


# ============================================================================
# MASTER RUNNER & CLI INTERFACE
# ============================================================================

def run_verification(
    skills_only: bool = False,
    staging_only: bool = False,
    build_only: bool = False,
    json_output: bool = False,
    strict: bool = False,
    root: Path = Path("dissertation.tex"),
    output: Path = Path("dissertation.pdf"),
    engine: str = "auto",
    verbose: bool = False,
) -> int:
    """Execute selected diagnostic passes and return process exit code (0 or 1)."""
    project_root = Path(__file__).resolve().parent
    t_start = time.perf_counter()

    # Determine which passes to run
    run_all = not (skills_only or staging_only or build_only)
    do_skills = run_all or skills_only
    do_staging = run_all or staging_only
    do_build = run_all or build_only

    pass_results: List[PassResult] = []

    # Check 1: Skills Schema
    if do_skills:
        pass_results.append(verify_skills(project_root, strict=strict, verbose=verbose))

    # Check 2: Staging Integration
    if do_staging:
        pass_results.append(verify_staging(project_root, strict=strict, verbose=verbose))

    # Check 3: Headless PDF Build
    if do_build:
        pass_results.append(verify_build(
            project_root=project_root,
            root_file=root,
            output_file=output,
            engine=engine,
            strict=strict,
            verbose=verbose
        ))

    total_duration_ms = (time.perf_counter() - t_start) * 1000
    overall_status = "FAIL" if any(p.status == "FAIL" for p in pass_results) else "PASS"

    # Render output
    if json_output:
        report_data = build_json_report(pass_results, total_duration_ms)
        print(json.dumps(report_data, indent=2))
    else:
        if HAS_RICH and console:
            render_rich_report(pass_results, total_duration_ms)
        else:
            render_plain_report(pass_results, total_duration_ms)

    return 0 if overall_status == "PASS" else 1


if HAS_RICH and "click" in sys.modules:
    @click.command()
    @click.option("--skills-only", is_flag=True, default=False,
                  help="Execute only Check 1: Skill YAML metadata validation (.agents/skills/).")
    @click.option("--staging-only", is_flag=True, default=False,
                  help="Execute only Check 2: Research sources staging integration (research_sources/).")
    @click.option("--build-only", is_flag=True, default=False,
                  help="Execute only Check 3: Headless end-to-end PDF compilation and zero broken refs.")
    @click.option("--json", "json_output", is_flag=True, default=False,
                  help="Output machine-readable JSON diagnostic summary.")
    @click.option("--strict", is_flag=True, default=False,
                  help="Enforce strict mode (treat all warnings as failures).")
    @click.option("--root", "-r", type=click.Path(path_type=Path), default=Path("dissertation.tex"),
                  help="Path to root LaTeX document (default: dissertation.tex).")
    @click.option("--output", "-o", type=click.Path(path_type=Path), default=Path("dissertation.pdf"),
                  help="Target output PDF filename (default: dissertation.pdf).")
    @click.option("--engine", "-e", type=click.Choice(["auto", "tectonic", "docker", "system"]), default="auto",
                  help="Compilation engine backend to invoke.")
    @click.option("--verbose", "-v", is_flag=True, default=False,
                  help="Display verbose diagnostics during verification.")
    def cli(
        skills_only: bool,
        staging_only: bool,
        build_only: bool,
        json_output: bool,
        strict: bool,
        root: Path,
        output: Path,
        engine: str,
        verbose: bool,
    ):
        """Automated Diagnostic & Verification CLI for Biology & Zoology Dissertation Suite."""
        exit_code = run_verification(
            skills_only=skills_only,
            staging_only=staging_only,
            build_only=build_only,
            json_output=json_output,
            strict=strict,
            root=root,
            output=output,
            engine=engine,
            verbose=verbose,
        )
        sys.exit(exit_code)
else:
    def cli():
        parser = argparse.ArgumentParser(
            description="Automated Diagnostic & Verification CLI for Biology & Zoology Dissertation Suite"
        )
        parser.add_argument("--skills-only", action="store_true",
                            help="Execute only Check 1: Skill YAML metadata validation.")
        parser.add_argument("--staging-only", action="store_true",
                            help="Execute only Check 2: Research sources staging integration.")
        parser.add_argument("--build-only", action="store_true",
                            help="Execute only Check 3: Headless PDF compilation and zero broken refs.")
        parser.add_argument("--json", dest="json_output", action="store_true",
                            help="Output machine-readable JSON diagnostic summary.")
        parser.add_argument("--strict", action="store_true",
                            help="Enforce strict mode (treat warnings as failures).")
        parser.add_argument("--root", "-r", type=Path, default=Path("dissertation.tex"),
                            help="Path to root LaTeX document.")
        parser.add_argument("--output", "-o", type=Path, default=Path("dissertation.pdf"),
                            help="Target output PDF filename.")
        parser.add_argument("--engine", "-e", choices=["auto", "tectonic", "docker", "system"], default="auto",
                            help="Compilation backend engine.")
        parser.add_argument("--verbose", "-v", action="store_true",
                            help="Display verbose diagnostics.")
        args = parser.parse_args()

        exit_code = run_verification(
            skills_only=args.skills_only,
            staging_only=args.staging_only,
            build_only=args.build_only,
            json_output=args.json_output,
            strict=args.strict,
            root=args.root,
            output=args.output,
            engine=args.engine,
            verbose=args.verbose,
        )
        sys.exit(exit_code)


if __name__ == "__main__":
    cli()
