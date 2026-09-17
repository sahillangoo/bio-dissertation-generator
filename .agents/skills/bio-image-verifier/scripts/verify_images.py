#!/usr/bin/env python3
"""Verify live LaTeX \\includegraphics paths, caption hygiene, and unused figure files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".pdf"}
BANNED_CAPTION = re.compile(
    r"(chatgpt|whatsapp|agarplate-|filename|\.jpeg|\.png|\.jpg)",
    re.IGNORECASE,
)
INCLUDE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
CAPTION_RE = re.compile(r"\\caption\{", re.DOTALL)
GRAPHICSPATH_RE = re.compile(r"\\graphicspath\{\{([^}]+)\}\}")


def resolve_input(project_root: Path, rel: str) -> Path:
    if not rel.endswith(".tex"):
        rel = rel + ".tex"
    return project_root / rel


def live_tex_files(project_root: Path, root_tex: Path) -> List[Path]:
    files: List[Path] = [root_tex]
    text = root_tex.read_text(encoding="utf-8", errors="replace")
    for match in INPUT_RE.finditer(text):
        path = resolve_input(project_root, match.group(1))
        if path.exists():
            files.append(path)
    return files


def graphics_dirs(project_root: Path, tex_files: List[Path]) -> List[Path]:
    dirs: List[Path] = [project_root / "figures"]
    for tf in tex_files:
        text = tf.read_text(encoding="utf-8", errors="replace")
        for match in GRAPHICSPATH_RE.finditer(text):
            dirs.append((project_root / match.group(1)).resolve())
    unique: List[Path] = []
    seen: Set[Path] = set()
    for d in dirs:
        if d not in seen:
            unique.append(d)
            seen.add(d)
    return unique


def find_image(name: str, search_dirs: List[Path]) -> Path | None:
    raw = Path(name)
    candidates = [raw] if raw.suffix else [raw.with_suffix(ext) for ext in IMAGE_EXTS]
    if raw.suffix:
        candidates = [raw]
    for directory in search_dirs:
        for cand in candidates:
            path = directory / cand.name if not cand.is_absolute() else cand
            if path.exists():
                return path
    return None


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        lines.append(re.sub(r"(?<!\\)%.*$", "", line))
    return "\n".join(lines)


def caption_snippets(text: str) -> List[str]:
    snippets: List[str] = []
    for match in re.finditer(r"\\caption\{", text):
        start = match.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        snippets.append(text[start : i - 1])
    return snippets


def audit(project_root: Path, root_tex: Path, figures_dir: Path) -> Dict[str, Any]:
    tex_files = live_tex_files(project_root, root_tex)
    search_dirs = graphics_dirs(project_root, tex_files)
    if figures_dir not in search_dirs:
        search_dirs.insert(0, figures_dir)

    includes: List[Dict[str, Any]] = []
    missing: List[Dict[str, str]] = []
    used_names: Set[str] = set()
    caption_flags: List[Dict[str, str]] = []

    for tf in tex_files:
        raw = tf.read_text(encoding="utf-8", errors="replace")
        text = strip_comments(raw)
        rel = str(tf.relative_to(project_root))
        for match in INCLUDE_RE.finditer(text):
            name = match.group(1).strip()
            path = find_image(name, search_dirs)
            rec = {"file": rel, "include": name, "resolved": str(path) if path else None}
            includes.append(rec)
            if path:
                used_names.add(path.name.lower())
            else:
                missing.append({"file": rel, "include": name})
        for cap in caption_snippets(text):
            if BANNED_CAPTION.search(cap):
                caption_flags.append({"file": rel, "caption": cap[:180]})

    unused: List[str] = []
    if figures_dir.exists():
        for p in sorted(figures_dir.iterdir()):
            if p.suffix.lower() in IMAGE_EXTS and p.name.lower() not in used_names:
                unused.append(p.name)

    status = "SUCCESS" if not missing and not caption_flags else "FAIL"
    return {
        "status": status,
        "live_tex_files": [str(p.relative_to(project_root)) for p in tex_files],
        "includes_count": len(includes),
        "missing_count": len(missing),
        "missing": missing,
        "caption_flags": caption_flags,
        "unused_figure_files": unused,
        "includes": includes,
    }


def write_markdown(report: Dict[str, Any]) -> str:
    lines = [
        "# Image verification",
        "",
        f"**Status:** {report['status']}",
        f"**Includes:** {report['includes_count']}",
        f"**Missing:** {report['missing_count']}",
        "",
        "## Missing files",
    ]
    if report["missing"]:
        for item in report["missing"]:
            lines.append(f"- `{item['file']}`: `{item['include']}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Caption hygiene"])
    if report["caption_flags"]:
        for item in report["caption_flags"]:
            lines.append(f"- `{item['file']}`: banned token in caption")
    else:
        lines.append("- none")
    lines.extend(["", "## Unused files in figures/"])
    if report["unused_figure_files"]:
        for name in report["unused_figure_files"]:
            lines.append(f"- `{name}`")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify dissertation figure files against live LaTeX includes."
    )
    parser.add_argument("--root", type=Path, default=Path("dissertation.tex"))
    parser.add_argument("--figures", type=Path, default=Path("figures"))
    parser.add_argument("--report", type=Path, default=Path("pipeline_outputs/image_verification.json"))
    parser.add_argument("--json", action="store_true", help="Print JSON to stdout")
    args = parser.parse_args()

    root_tex = args.root.resolve()
    project_root = root_tex.parent
    figures_dir = args.figures if args.figures.is_absolute() else project_root / args.figures
    report = audit(project_root, root_tex, figures_dir.resolve())

    report_path = args.report if args.report.is_absolute() else project_root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path = report_path.with_suffix(".md")
    md_path.write_text(write_markdown(report), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(write_markdown(report))
        print(f"Wrote {report_path}")

    return 0 if report["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
