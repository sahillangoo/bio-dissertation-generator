"""
T1-AGENT: Contract tests for repository-local Cursor agents under .cursor/agents/.

TDD RED phase: defines the coordinator + specialist audit workflow before agent
definitions are implemented.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import PROJECT_ROOT, parse_yaml_frontmatter

AGENTS_DIR = PROJECT_ROOT / ".cursor" / "agents"

COORDINATOR_AGENT = "dissertation-fixer"

REQUIRED_AGENT_FILES = (
    "dissertation-fixer.md",
    "content-auditor.md",
    "citation-auditor.md",
    "layout-auditor.md",
    "image-verifier.md",
    "final-reviewer.md",
)

READONLY_SPECIALIST_STEMS = (
    "content-auditor",
    "citation-auditor",
    "layout-auditor",
    "image-verifier",
    "final-reviewer",
)

COORDINATOR_VERIFICATION_COMMANDS = (
    "uv run pytest tests/test_agent_definitions.py tests/test_skills_schema.py tests/test_pipeline_cli.py -q",
    "uv run python verify.py",
    "uv run python pipeline.py --all",
)

LOWERCASE_HYPHEN_NAME = re.compile(r"^[a-z0-9-]+$")

FINDING_SCHEMA_LABELS = (
    "**Severity**:",
    "**File/Location**:",
    "**Issue**:",
    "**Evidence**:",
    "**Recommended correction**:",
)

# Documented examples for agent authors; equivalent placeholder wording is allowed.
FINDING_PLACEHOLDER_EXAMPLES = (
    "<critical|major|minor>",
    "<path:line or section>",
    "<observed problem>",
    "<source or build evidence>",
    "<specific safe change>",
)

FINDING_SCHEMA_SECTION_HEADINGS = (
    "finding output format",
    "finding format",
    "finding schema",
    "structured findings",
)

PARALLEL_DELEGATION_SECTION_HEADINGS = (
    "parallel delegation",
    "specialist delegation",
    "delegation workflow",
)

SAFETY_POLICY_SECTION_HEADINGS = (
    "safety and edit policy",
    "edit policy",
    "safety policy",
)

CORRECTIVE_RERUN_SECTION_HEADINGS = (
    "corrective rerun limit",
    "corrective rerun policy",
    "bounded rerun",
)

SAFETY_POLICY_DIRECTIVES = (
    "apply only evidence-backed fixes",
    "record candidate-supplied gaps",
    "use repository evidence for manuscript edits",
)

CONTENT_AUDITOR_SKILL_SECTION_HEADINGS = (
    "required skills",
    "skill requirements",
    "mandatory skills",
)

CONTENT_AUDITOR_SKILL_PATHS = (
    ".agents/skills/dissertation-checker/SKILL.md",
    ".agents/skills/scholar-language-auditor/SKILL.md",
)

FINAL_REVIEWER_SECTION_HEADINGS = (
    "final verification",
    "independent review",
    "post-fix verification",
)

FINAL_REVIEWER_DIRECTIVES = (
    "rerun dissertation-checker",
    "confirm scholar-language-auditor constraints",
)

COORDINATOR_EDIT_AUTHORITY_DIRECTIVES = (
    "may edit live manuscript files",
    "coordinator applies manuscript fixes",
)

PARALLEL_DELEGATION_DIRECTIVES = (
    "delegate",
    "parallel",
)

SHELL_CODE_FENCE_LANGS = frozenset({"", "bash", "sh", "shell", "powershell", "zsh"})

READONLY_CHECKLIST_GUARD = re.compile(
    r"\b(?:checklist-only|checklist only|read-only|read only|findings only|audit only)\b",
    re.IGNORECASE,
)

SKILL_DOCUMENTS_IN_FULL_DIRECTIVE = re.compile(
    r"\bapply\b.{0,120}\bskill documents?\b.{0,120}\bin full\b",
    re.IGNORECASE,
)

RUN_VERIFIER_WORKFLOW_DIRECTIVE = re.compile(
    r"^run\b.{0,120}\b(?:verifier script|verify_images\.py)\b",
    re.IGNORECASE,
)

READONLY_FORBIDDEN_SCRIPT = re.compile(
    r"\b(?:verify_images\.py|verify\.py|pipeline\.py|build\.py)\b",
    re.IGNORECASE,
)

INITIAL_PARALLEL_SPECIALISTS = (
    "content-auditor",
    "citation-auditor",
    "layout-auditor",
    "image-verifier",
)

LIVE_DISCOVERY_SECTION_HEADINGS = (
    "live manuscript discovery",
    "live file discovery",
    "manuscript discovery",
)

DIRTY_TARGET_PREFLIGHT_SECTION_HEADINGS = (
    "dirty-target preflight",
    "worktree preflight",
    "preflight before mutation",
)

PIPELINE_DIAGNOSTICS_SECTION_HEADINGS = (
    "pipeline diagnostics",
    "pipeline report handling",
    "pipeline outputs policy",
)

BUILD_VALIDATION_WORKFLOW_SECTION_HEADINGS = (
    "build and validation workflow",
    "verification workflow",
    "build validation workflow",
)

CONSOLIDATED_REPORT_SECTION_HEADINGS = (
    "consolidated repair report",
    "repair report",
)

DELEGATION_ACCESS_SECTION_HEADINGS = (
    "delegation access",
    "direct-child delegation",
    "task access precondition",
)

CONSOLIDATED_REPORT_SECTION_LABELS = (
    "**Changes**",
    "**Evidence**",
    "**Candidate gaps**",
    "**Validation**",
    "**Residual findings**",
)

MUTATING_COMMAND_AFTER_VERIFY = re.compile(
    r"\b(?:uv run python pipeline\.py|uv run python build\.py|pipeline\.py|build\.py)\b",
    re.IGNORECASE,
)

# Original image-verifier multiline command (regression fixture).
SYNTHETIC_MULTILINE_VERIFY_IMAGES_FENCE = """```bash
uv run python .agents/skills/bio-image-verifier/scripts/verify_images.py --root dissertation.tex \\
  --figures figures \\
  --report pipeline_outputs/image_verification.json
```"""

NEGATED_DIRECTIVE_PREFIX = re.compile(
    r"^\s*(?:do not|don't|never|not)\b",
    re.IGNORECASE,
)

FORBIDDEN_PLACEHOLDER_TERMS = re.compile(
    r"\b(?:prohibited|unavailable|omit)\b",
    re.IGNORECASE,
)

RERUN_CAP_SENTENCE = re.compile(
    r"^\s*At most one corrective rerun\s*[.!?]\s*$",
    re.IGNORECASE | re.MULTILINE,
)

RERUN_FORBIDDEN_LANGUAGE = re.compile(
    r"\b(?:unlimited|multiple|do not|don't|never)\b",
    re.IGNORECASE,
)

FORBIDDEN_RERUN_QUANTITY_PATTERNS = (
    re.compile(r"\btwo\b[^.\n]{0,80}\bcorrective\b[^.\n]{0,40}\brerun", re.I),
    re.compile(r"\bthree\b[^.\n]{0,80}\bcorrective\b[^.\n]{0,40}\brerun", re.I),
    re.compile(r"\b(?:four|five|six|seven|eight|nine|ten)\b[^.\n]{0,80}\bcorrective\b", re.I),
    re.compile(r"\b[2-9]\b[^.\n]{0,40}\bcorrective\b[^.\n]{0,40}\brerun", re.I),
    re.compile(r"\bup to (?:two|three|[2-9])\b[^.\n]{0,60}\bcorrective\b", re.I),
    re.compile(r"\bat least two\b[^.\n]{0,60}\bcorrective\b[^.\n]{0,40}\brerun", re.I),
)

HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)

FINDING_LINE_PATTERNS = tuple(
    re.compile(
        rf"^\s*(?:[-*+]\s+)?{re.escape(label)}\s*(?P<placeholder><[^>]+>)\s*$",
        re.IGNORECASE,
    )
    for label in FINDING_SCHEMA_LABELS
)


def _agent_body(agent_path: Path) -> str:
    text = agent_path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) >= 3:
        return parts[2]
    return text


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _heading_key(title: str) -> str:
    lowered = title.lower()
    return _normalize(re.sub(r"[^a-z0-9]+", " ", lowered)).strip()


def _section_by_heading_keys(body: str, heading_keys: tuple[str, ...]) -> str | None:
    matches = list(HEADING_RE.finditer(body))
    if not matches:
        return None
    wanted = {_heading_key(h) for h in heading_keys}
    for idx, match in enumerate(matches):
        title = match.group(1)
        if _heading_key(title) not in wanted:
            continue
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        return body[start:end]
    return None


def _strip_list_marker(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or stripped.startswith("```"):
        return None
    bullet = re.match(r"^[-*+]\s+(.*)$", stripped)
    if bullet:
        return bullet.group(1).strip()
    numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
    if numbered:
        return numbered.group(1).strip()
    return stripped


def _affirmative_directive_lines(section: str) -> list[str]:
    """Bullet/list items and standalone imperative lines that are not negated."""
    directives: list[str] = []
    for raw_line in section.splitlines():
        content = _strip_list_marker(raw_line)
        if content is None:
            continue
        if NEGATED_DIRECTIVE_PREFIX.match(content):
            continue
        directives.append(content)
    return directives


def _assert_required_affirmative_directives(
    section: str,
    phrases: tuple[str, ...],
    *,
    context: str,
) -> None:
    norm_directives = [_normalize(line) for line in _affirmative_directive_lines(section)]
    for phrase in phrases:
        norm_phrase = _normalize(phrase)
        matched = any(line.startswith(norm_phrase) for line in norm_directives)
        assert matched, (
            f"{context}: missing affirmative directive starting with {phrase!r}; "
            f"expected its own list item or standalone imperative line "
            f"(negated lines do not count)"
        )


def _markdown_list_items(section: str) -> list[str]:
    items: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if re.match(r"^[-*+]\s+", stripped):
            items.append(re.sub(r"^[-*+]\s+", "", stripped).strip())
        elif re.match(r"^\d+\.\s+", stripped):
            items.append(re.sub(r"^\d+\.\s+", "", stripped).strip())
    return items


def _valid_finding_placeholder(placeholder: str) -> bool:
    inner = placeholder[1:-1].strip()
    if not inner:
        return False
    return FORBIDDEN_PLACEHOLDER_TERMS.search(inner) is None


def _finding_line_matches(line: str, pattern: re.Pattern[str]) -> bool:
    match = pattern.match(line.rstrip())
    if not match:
        return False
    placeholder = match.group("placeholder")
    return _valid_finding_placeholder(placeholder)


def _has_consecutive_finding_template_block(section: str) -> bool:
    lines = section.splitlines()
    block_len = len(FINDING_LINE_PATTERNS)
    if len(lines) < block_len:
        return False
    for start in range(len(lines) - block_len + 1):
        block = lines[start : start + block_len]
        if all(
            _finding_line_matches(line, pattern)
            for pattern, line in zip(FINDING_LINE_PATTERNS, block, strict=True)
        ):
            return True
    return False


def _assert_section_contract(
    body: str,
    heading_keys: tuple[str, ...],
    *,
    context: str,
    required_directives: tuple[str, ...] | None = None,
    required_list_tokens: tuple[str, ...] | None = None,
) -> str:
    section = _section_by_heading_keys(body, heading_keys)
    assert section is not None, (
        f"{context}: missing section with heading matching one of {heading_keys!r}"
    )
    if required_directives:
        _assert_required_affirmative_directives(
            section, required_directives, context=context
        )
    if required_list_tokens:
        norm_items = _normalize("\n".join(_markdown_list_items(section)))
        norm_section = _normalize(section)
        missing_tokens = [
            token
            for token in required_list_tokens
            if _normalize(token) not in norm_items and _normalize(token) not in norm_section
        ]
        assert not missing_tokens, (
            f"{context}: section list/body missing required entries {missing_tokens!r}"
        )
    return section


def _assert_finding_schema_contract(body: str, agent_stem: str) -> None:
    section = _section_by_heading_keys(body, FINDING_SCHEMA_SECTION_HEADINGS)
    assert section is not None, (
        f"{agent_stem}: missing finding schema section "
        f"(expected heading like 'Finding output format')"
    )
    assert _has_consecutive_finding_template_block(section), (
        f"{agent_stem}: finding schema must contain five consecutive lines with labels "
        f"{FINDING_SCHEMA_LABELS!r} and nonempty angle-bracket placeholders "
        f"(examples {FINDING_PLACEHOLDER_EXAMPLES!r}; no prohibited/unavailable/omit inside)"
    )


def _assert_corrective_rerun_limit(body: str, context: str) -> None:
    section = _section_by_heading_keys(body, CORRECTIVE_RERUN_SECTION_HEADINGS)
    assert section is not None, (
        f"{context}: missing corrective rerun section "
        f"(expected heading like 'Corrective rerun limit')"
    )

    cap_match = RERUN_CAP_SENTENCE.search(section)
    assert cap_match is not None, (
        f"{context}: corrective rerun section must include a standalone sentence "
        f"starting with 'At most one corrective rerun' and ending with . ! or ?"
    )

    forbidden = RERUN_FORBIDDEN_LANGUAGE.search(section)
    assert forbidden is None, (
        f"{context}: corrective rerun section must not contain {forbidden.group()!r}"
    )

    for pattern in FORBIDDEN_RERUN_QUANTITY_PATTERNS:
        assert not pattern.search(section), (
            f"{context}: corrective rerun section must not allow more than one rerun; "
            f"matched forbidden pattern {pattern.pattern!r}"
        )


def _frontmatter_readonly_is_true(data: dict) -> bool:
    readonly = data.get("readonly")
    return readonly is True or str(readonly).strip().lower() == "true"


def _normalize_shell_command(command: str) -> str:
    return re.sub(r"\s+", " ", command.strip())


def _join_shell_block_lines(block_lines: list[str]) -> list[str]:
    """Split a fenced shell block into logical commands, honoring \\ and PowerShell ` continuations."""
    commands: list[str] = []
    buffer: list[str] = []
    for raw_line in block_lines:
        stripped = raw_line.rstrip()
        if not stripped or stripped.lstrip().startswith("#"):
            if buffer:
                commands.append(_normalize_shell_command(" ".join(buffer)))
                buffer = []
            continue
        line = stripped
        continued = False
        if line.endswith("\\"):
            line = line[:-1].rstrip()
            continued = True
        elif line.endswith("`"):
            line = line[:-1].rstrip()
            continued = True
        buffer.append(line)
        if not continued:
            commands.append(_normalize_shell_command(" ".join(buffer)))
            buffer = []
    if buffer:
        commands.append(_normalize_shell_command(" ".join(buffer)))
    return [cmd for cmd in commands if cmd]


def _iter_shell_commands_from_fences(body: str) -> list[str]:
    commands: list[str] = []
    in_code = False
    code_lang = ""
    block_lines: list[str] = []
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            if in_code:
                if code_lang in SHELL_CODE_FENCE_LANGS:
                    commands.extend(_join_shell_block_lines(block_lines))
                block_lines = []
                in_code = False
                code_lang = ""
            else:
                in_code = True
                code_lang = stripped[3:].strip().lower()
            continue
        if in_code:
            block_lines.append(raw_line)
    return commands


def _shell_command_directs_readonly_forbidden_execution(command: str) -> bool:
    return READONLY_FORBIDDEN_SCRIPT.search(command) is not None


def _iter_directive_lines_for_mutating_audit(body: str) -> list[tuple[str, str]]:
    """List/markdown imperatives and joined shell fence commands subject to mutating checks."""
    directives: list[tuple[str, str]] = []
    for command in _iter_shell_commands_from_fences(body):
        directives.append(("code", command))
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("```"):
            continue
        content = _strip_list_marker(raw_line)
        if content is None:
            continue
        if re.match(r"^[-*+]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            directives.append(("list", content))
            continue
        if re.match(r"^(?:run|execute|apply|invoke|use)\b", content, re.IGNORECASE):
            directives.append(("imperative", content))
    return directives


def _line_directs_uv_run_verify(line: str, kind: str) -> bool:
    if re.search(r"\bverify\.py\b", line, re.IGNORECASE) and kind == "code":
        return True
    if not re.search(r"\buv run python verify\.py\b", line, re.IGNORECASE):
        return False
    start = line.strip()
    if re.match(r"^uv run\b", start, re.IGNORECASE):
        return True
    if re.match(r"^(?:run|execute|invoke)\b", start, re.IGNORECASE):
        return True
    return False


def _line_directs_uv_run_pipeline(line: str, kind: str) -> bool:
    if re.search(r"\bpipeline\.py\b", line, re.IGNORECASE) and kind == "code":
        return True
    if not re.search(r"\buv run python pipeline\.py\b", line, re.IGNORECASE):
        return False
    start = line.strip()
    if re.match(r"^uv run\b", start, re.IGNORECASE):
        return True
    if re.match(r"^(?:run|execute|invoke)\b", start, re.IGNORECASE):
        return True
    return False


def _line_directs_verifier_report_command(line: str, kind: str) -> bool:
    if kind != "code":
        return False
    return (
        _shell_command_directs_readonly_forbidden_execution(line)
        and re.search(r"--report\b", line, re.IGNORECASE) is not None
    )


def _line_directs_checker_rerun_without_readonly_guard(line: str) -> bool:
    if not re.search(r"\brerun dissertation-checker\b", line, re.IGNORECASE):
        return False
    return READONLY_CHECKLIST_GUARD.search(line) is None


def _coordinator_body() -> str:
    agent_path = AGENTS_DIR / f"{COORDINATOR_AGENT}.md"
    assert agent_path.is_file(), f"Coordinator agent missing: {agent_path}"
    return _agent_body(agent_path)


def _section_text(body: str, heading_keys: tuple[str, ...]) -> str:
    section = _section_by_heading_keys(body, heading_keys)
    assert section is not None, (
        f"Missing coordinator section matching one of {heading_keys!r}"
    )
    return section


def _ordered_shell_commands(section: str) -> list[str]:
    return [_normalize(cmd) for cmd in _iter_shell_commands_from_fences(section)]


def _command_index(commands: list[str], needle: str) -> int:
    norm_needle = _normalize(needle)
    for index, command in enumerate(commands):
        if norm_needle in command:
            return index
    return -1


def _assert_coordinator_live_discovery_contract(section: str) -> None:
    norm = _normalize(section)
    assert "dissertation.tex" in norm, "discovery must anchor on dissertation.tex"
    assert "\\input" in section or "input" in norm, "discovery must reference \\input"
    assert "\\include" in section or "include" in norm, "discovery must reference \\include"
    assert "recursive" in norm, "discovery must describe recursive resolution"


def _assert_coordinator_dirty_target_preflight(section: str) -> None:
    norm = _normalize(section)
    assert "git status" in norm, "preflight must inspect git status"
    has_out_of_repo_backup = (
        "outside the repository" in norm
        or "outside repo" in norm
        or "outside repository" in norm
    )
    has_backup_or_hash = "backup" in norm or "hash" in norm
    assert has_out_of_repo_backup and has_backup_or_hash, (
        "preflight must describe recoverable backup/hash stored outside the repository"
    )
    assert "before" in norm and (
        "pipeline" in norm or "build" in norm or "mutating" in norm
    ), "preflight must run before mutating pipeline/build commands"
    assert "generated artifact" in norm or "artifact replacement" in norm, (
        "preflight must address intended generated artifact replacement"
    )


def _assert_coordinator_pipeline_diagnostics_policy(section: str) -> None:
    norm = _normalize(section)
    assert "diagnostic" in norm, "pipeline outputs must be treated as diagnostics"
    assert "morphology" in norm or "iacuc" in norm, (
        "policy must name the morphology/IACUC stub"
    )
    assert "quarantine" in norm or "reject" in norm, (
        "stub must be quarantined or rejected, not used as evidence"
    )


def _assert_coordinator_build_validation_command_order(section: str) -> None:
    commands = _ordered_shell_commands(section)
    assert commands, "build/validation workflow must list shell commands in order"
    pipeline_idx = _command_index(commands, "uv run python pipeline.py --all")
    verify_idx = _command_index(commands, "uv run python verify.py")
    assert pipeline_idx >= 0, "workflow must include uv run python pipeline.py --all"
    assert verify_idx >= 0, "workflow must include uv run python verify.py"
    assert pipeline_idx < verify_idx, (
        "pipeline.py --all must occur before final uv run python verify.py"
    )
    for command in commands[verify_idx + 1 :]:
        assert not MUTATING_COMMAND_AFTER_VERIFY.search(command), (
            "no mutating build/pipeline command may follow verify.py before final-reviewer"
        )


def _assert_coordinator_parallel_wave_contract(section: str) -> None:
    norm = _normalize(section)
    for stem in INITIAL_PARALLEL_SPECIALISTS:
        assert stem in norm, f"initial parallel wave must include {stem!r}"
    assert "parallel" in norm, "coordinator must describe parallel launch"
    assert "initial wave" in norm or "one initial wave" in norm, (
        "coordinator must define an initial parallel wave"
    )
    initial_wave_lines = [
        line
        for line in section.splitlines()
        if "initial wave" in _normalize(line) or "parallel-launch" in _normalize(line)
    ]
    if initial_wave_lines:
        joined_initial = _normalize(" ".join(initial_wave_lines))
        assert "final-reviewer" not in joined_initial, (
            "final-reviewer must not appear in the initial parallel wave line"
        )
    assert "final-reviewer" in norm, "coordinator must delegate final-reviewer"
    assert "post-fix" in norm or "post fix" in norm, (
        "final-reviewer must be explicitly post-fix"
    )
    assert "post-verification" in norm or "post verification" in norm or "validation" in norm, (
        "final-reviewer must run after verification/build validation"
    )


def _assert_coordinator_consolidated_report_contract(section: str) -> None:
    for label in CONSOLIDATED_REPORT_SECTION_LABELS:
        assert label in section, f"consolidated report must include section label {label!r}"


def _assert_coordinator_delegation_access_precondition(section: str) -> None:
    norm = _normalize(section)
    has_direct_child = "direct-child" in norm or "direct child" in norm
    has_task_access = "task" in norm and ("access" in norm or "delegation" in norm)
    assert has_direct_child or has_task_access, (
        "coordinator must require direct-child delegation or Task access"
    )
    assert "stop" in norm and "report" in norm, (
        "coordinator must stop and report when delegation access is unavailable"
    )


def _assert_coordinator_corrective_rerun_conditional(section: str) -> None:
    norm = _normalize(section)
    assert "at most one corrective rerun" in norm, (
        "corrective rerun section must cap reruns at one"
    )
    assert "supported residual" in norm or "supported residuals" in norm, (
        "corrective rerun must be conditional on supported residuals"
    )


def _assert_readonly_specialist_no_mutating_directives(body: str, stem: str) -> None:
    violations: list[str] = []
    for kind, line in _iter_directive_lines_for_mutating_audit(body):
        if kind == "code" and _shell_command_directs_readonly_forbidden_execution(line):
            violations.append(f"shell fence executes forbidden script: {line!r}")
            continue
        if _line_directs_uv_run_verify(line, kind):
            violations.append(f"directs verify.py execution: {line!r}")
        if _line_directs_uv_run_pipeline(line, kind):
            violations.append(f"directs pipeline.py execution: {line!r}")
        if _line_directs_verifier_report_command(line, kind):
            violations.append(f"directs verifier --report command: {line!r}")
        if SKILL_DOCUMENTS_IN_FULL_DIRECTIVE.search(line):
            violations.append(f"directs applying skills in full: {line!r}")
        if RUN_VERIFIER_WORKFLOW_DIRECTIVE.match(line.strip()):
            violations.append(f"directs running verifier workflow: {line!r}")
        if _line_directs_checker_rerun_without_readonly_guard(line):
            violations.append(
                f"rerun dissertation-checker without checklist-only/read-only guard: {line!r}"
            )
    assert not violations, (
        f"{stem}: read-only specialist must not direct mutating workflows; "
        f"fix directive lines (artifact path mentions without execution are allowed):\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


@pytest.fixture(scope="module")
def agents_dir() -> Path:
    return AGENTS_DIR


def test_agents_directory_exists(agents_dir: Path) -> None:
    """T1-AGENT-01: .cursor/agents/ exists and is a directory."""
    assert agents_dir.exists(), f"Agents directory missing: {agents_dir}"
    assert agents_dir.is_dir(), f"Agents path is not a directory: {agents_dir}"


def test_required_agent_inventory_subset(agents_dir: Path) -> None:
    """T1-AGENT-02: Required dissertation agents exist; extra custom agents are allowed."""
    assert agents_dir.is_dir(), f"Agents directory missing: {agents_dir}"
    present = {p.name for p in agents_dir.glob("*.md")}
    missing = sorted(set(REQUIRED_AGENT_FILES) - present)
    assert not missing, f"Missing required agent definition files: {missing}"


@pytest.mark.parametrize("filename", REQUIRED_AGENT_FILES)
def test_agent_filename_and_frontmatter_name_match(filename: str) -> None:
    """T1-AGENT-03: Filename stem is lowercase-hyphenated and matches frontmatter name."""
    agent_path = AGENTS_DIR / filename
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"

    stem = agent_path.stem
    assert LOWERCASE_HYPHEN_NAME.match(stem), (
        f"Agent filename stem must be lowercase-hyphenated, got: {stem!r}"
    )

    data = parse_yaml_frontmatter(agent_path)
    assert "name" in data, f"'name' missing in frontmatter of {agent_path}"
    name = str(data["name"]).strip()
    assert name == stem, (
        f"Frontmatter name {name!r} must match filename stem {stem!r} in {agent_path}"
    )


@pytest.mark.parametrize("filename", REQUIRED_AGENT_FILES)
def test_agent_frontmatter_description_and_model(filename: str) -> None:
    """T1-AGENT-04: Every agent declares a nonempty description and model: inherit."""
    agent_path = AGENTS_DIR / filename
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"

    data = parse_yaml_frontmatter(agent_path)
    desc = data.get("description")
    assert isinstance(desc, str) and desc.strip(), (
        f"Nonempty 'description' required in {agent_path}"
    )

    model = data.get("model")
    assert model is not None, f"'model' field missing in {agent_path}"
    assert str(model).strip().lower() == "inherit", (
        f"'model' must be inherit in {agent_path}, got: {model!r}"
    )


def test_readonly_shell_fence_detects_multiline_verify_images_with_report() -> None:
    """Regression: joined bash continuations must flag verify_images.py + --report."""
    body = f"## Procedure (read-only)\n\n{SYNTHETIC_MULTILINE_VERIFY_IMAGES_FENCE}\n"
    commands = _iter_shell_commands_from_fences(body)
    assert len(commands) == 1
    assert "--report" in commands[0]
    assert "verify_images.py" in commands[0]
    with pytest.raises(AssertionError, match="shell fence executes forbidden script"):
        _assert_readonly_specialist_no_mutating_directives(body, "synthetic-image-verifier")


@pytest.mark.parametrize("stem", READONLY_SPECIALIST_STEMS)
def test_readonly_specialists_forbid_mutating_directives(stem: str) -> None:
    """T1-AGENT-05b: Read-only specialists must not direct verify/pipeline runs or full skill edits."""
    agent_path = AGENTS_DIR / f"{stem}.md"
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"
    _assert_readonly_specialist_no_mutating_directives(_agent_body(agent_path), stem)


@pytest.mark.parametrize("stem", READONLY_SPECIALIST_STEMS)
def test_readonly_specialists_declare_readonly_true(stem: str) -> None:
    """T1-AGENT-05: Audit specialists are read-only (readonly: true)."""
    agent_path = AGENTS_DIR / f"{stem}.md"
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"

    data = parse_yaml_frontmatter(agent_path)
    assert _frontmatter_readonly_is_true(data), (
        f"{stem} must declare readonly: true in frontmatter, got: {data.get('readonly')!r}"
    )


def test_coordinator_declares_manuscript_edit_authority() -> None:
    """T1-AGENT-06: Coordinator has explicit writable authority (not readonly: true)."""
    agent_path = AGENTS_DIR / f"{COORDINATOR_AGENT}.md"
    assert agent_path.is_file(), f"Coordinator agent missing: {agent_path}"

    data = parse_yaml_frontmatter(agent_path)
    assert not _frontmatter_readonly_is_true(data), (
        f"{COORDINATOR_AGENT} must not declare readonly: true"
    )

    body = _agent_body(agent_path)
    _assert_section_contract(
        body,
        SAFETY_POLICY_SECTION_HEADINGS,
        context=f"{COORDINATOR_AGENT} edit authority",
        required_directives=COORDINATOR_EDIT_AUTHORITY_DIRECTIVES,
    )


@pytest.mark.parametrize("stem", READONLY_SPECIALIST_STEMS)
def test_specialist_structured_finding_schema(stem: str) -> None:
    """T1-AGENT-07: Specialists document five consecutive finding template lines."""
    agent_path = AGENTS_DIR / f"{stem}.md"
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"
    _assert_finding_schema_contract(_agent_body(agent_path), stem)


def test_content_auditor_required_skills_section() -> None:
    """T1-AGENT-08: Content auditor lists mandatory checker skills in a skills section."""
    agent_path = AGENTS_DIR / "content-auditor.md"
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"
    body = _agent_body(agent_path)
    _assert_section_contract(
        body,
        CONTENT_AUDITOR_SKILL_SECTION_HEADINGS,
        context="content-auditor skills",
        required_list_tokens=CONTENT_AUDITOR_SKILL_PATHS,
    )


def test_final_reviewer_verification_section() -> None:
    """T1-AGENT-09: Final reviewer section mandates checker rerun and language audit."""
    agent_path = AGENTS_DIR / "final-reviewer.md"
    assert agent_path.is_file(), f"Agent file missing: {agent_path}"
    body = _agent_body(agent_path)
    _assert_section_contract(
        body,
        FINAL_REVIEWER_SECTION_HEADINGS,
        context="final-reviewer verification",
        required_directives=FINAL_REVIEWER_DIRECTIVES,
    )


def test_coordinator_parallel_delegation_section_lists_specialists() -> None:
    """T1-AGENT-10: Coordinator delegation section lists every specialist for parallel launch."""
    agent_path = AGENTS_DIR / f"{COORDINATOR_AGENT}.md"
    assert agent_path.is_file(), f"Coordinator agent missing: {agent_path}"
    body = _agent_body(agent_path)
    section = _assert_section_contract(
        body,
        PARALLEL_DELEGATION_SECTION_HEADINGS,
        context=f"{COORDINATOR_AGENT} delegation",
        required_list_tokens=READONLY_SPECIALIST_STEMS,
    )
    _assert_required_affirmative_directives(
        section,
        PARALLEL_DELEGATION_DIRECTIVES,
        context=f"{COORDINATOR_AGENT} delegation",
    )


def test_coordinator_safety_policy_and_rerun_limit_sections() -> None:
    """T1-AGENT-11: Coordinator safety section uses positive directives and one-rerun cap."""
    agent_path = AGENTS_DIR / f"{COORDINATOR_AGENT}.md"
    assert agent_path.is_file(), f"Coordinator agent missing: {agent_path}"
    body = _agent_body(agent_path)

    _assert_section_contract(
        body,
        SAFETY_POLICY_SECTION_HEADINGS,
        context=f"{COORDINATOR_AGENT} safety policy",
        required_directives=SAFETY_POLICY_DIRECTIVES,
    )
    _assert_corrective_rerun_limit(body, f"{COORDINATOR_AGENT} rerun policy")


def test_coordinator_live_manuscript_discovery_contract() -> None:
    """T1-AGENT-13: Recursive live discovery from dissertation.tex input/include tree."""
    body = _coordinator_body()
    _assert_coordinator_live_discovery_contract(
        _section_text(body, LIVE_DISCOVERY_SECTION_HEADINGS)
    )


def test_coordinator_dirty_target_preflight_contract() -> None:
    """T1-AGENT-14: Preflight git status and out-of-repo backup before mutating builds."""
    body = _coordinator_body()
    _assert_coordinator_dirty_target_preflight(
        _section_text(body, DIRTY_TARGET_PREFLIGHT_SECTION_HEADINGS)
    )


def test_coordinator_pipeline_reports_diagnostics_only_contract() -> None:
    """T1-AGENT-15: Pipeline reports are diagnostics; morphology/IACUC stub quarantined."""
    body = _coordinator_body()
    _assert_coordinator_pipeline_diagnostics_policy(
        _section_text(body, PIPELINE_DIAGNOSTICS_SECTION_HEADINGS)
    )


def test_coordinator_build_validation_command_order_contract() -> None:
    """T1-AGENT-16: pipeline.py --all before verify.py; no mutating commands after verify."""
    body = _coordinator_body()
    _assert_coordinator_build_validation_command_order(
        _section_text(body, BUILD_VALIDATION_WORKFLOW_SECTION_HEADINGS)
    )


def test_coordinator_initial_parallel_wave_contract() -> None:
    """T1-AGENT-17: Initial wave is four auditors; final-reviewer is post-fix/post-verification."""
    body = _coordinator_body()
    _assert_coordinator_parallel_wave_contract(
        _section_text(body, PARALLEL_DELEGATION_SECTION_HEADINGS)
    )


def test_coordinator_consolidated_report_required_sections() -> None:
    """T1-AGENT-18: Consolidated repair report lists required section labels."""
    body = _coordinator_body()
    _assert_coordinator_consolidated_report_contract(
        _section_text(body, CONSOLIDATED_REPORT_SECTION_HEADINGS)
    )


def test_coordinator_delegation_task_access_precondition() -> None:
    """T1-AGENT-19: Direct-child/Task delegation access required; stop and report if missing."""
    body = _coordinator_body()
    _assert_coordinator_delegation_access_precondition(
        _section_text(body, DELEGATION_ACCESS_SECTION_HEADINGS)
    )


def test_coordinator_corrective_rerun_conditional_on_supported_residuals() -> None:
    """T1-AGENT-20: Corrective rerun runs only for supported residuals."""
    body = _coordinator_body()
    _assert_coordinator_corrective_rerun_conditional(
        _section_text(body, CORRECTIVE_RERUN_SECTION_HEADINGS)
    )


def test_readonly_shell_fence_detects_build_py_execution() -> None:
    """Regression: readonly specialists must not execute build.py from shell fences."""
    body = "## Procedure\n\n```bash\nuv run python build.py\n```\n"
    with pytest.raises(AssertionError, match="shell fence executes forbidden script"):
        _assert_readonly_specialist_no_mutating_directives(body, "synthetic-build-runner")


@pytest.mark.parametrize("command", COORDINATOR_VERIFICATION_COMMANDS)
def test_coordinator_lists_exact_verification_commands(command: str) -> None:
    """T1-AGENT-12: Coordinator documents the plan's verification commands verbatim."""
    agent_path = AGENTS_DIR / f"{COORDINATOR_AGENT}.md"
    assert agent_path.is_file(), f"Coordinator agent missing: {agent_path}"
    body = _agent_body(agent_path)
    assert command in body, (
        f"Coordinator must include verification command exactly:\n  {command!r}"
    )
