#!/usr/bin/env python3
"""
run_pipeline.py - Wrapper script for the Final Output dissertation pipeline.
Executes the master pipeline orchestrator (pipeline.py) located at the project root.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Final Output Dissertation Pipeline Wrapper CLI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute all 7 pipeline stages sequentially.",
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="",
        help="Execute a specific stage (e.g. staging, biology_logic, adversarial_review, final_build).",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="List all 7 pipeline stages with descriptions.",
    )
    parser.add_argument(
        "--audit-skills",
        action="store_true",
        help="Audit all installed skills, detect duplicates, and generate bifurcated catalog.",
    )
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="Alias for --audit-skills.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Display the latest pipeline state checkpoint.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean intermediate artifacts in pipeline_outputs/ before running.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format.",
    )

    args = parser.parse_args()

    # Locate project root pipeline.py
    skill_dir = Path(__file__).resolve().parent.parent
    project_root = skill_dir.parent.parent.parent
    pipeline_py = project_root / "pipeline.py"

    if not pipeline_py.exists():
        print(f"[ERROR] Root pipeline script not found at {pipeline_py}", file=sys.stderr)
        return 1

    forward_args = [sys.executable, str(pipeline_py)]
    if args.all:
        forward_args.append("--all")
    if args.stage:
        forward_args.extend(["--stage", args.stage])
    if args.list_stages:
        forward_args.append("--list-stages")
    if args.audit_skills:
        forward_args.append("--audit-skills")
    if args.list_skills:
        forward_args.append("--list-skills")
    if args.status:
        forward_args.append("--status")
    if args.clean:
        forward_args.append("--clean")
    if args.json:
        forward_args.append("--json")

    # If no flag was passed, default to --help
    if len(forward_args) == 2:
        forward_args.append("--help")

    res = subprocess.run(forward_args)
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
