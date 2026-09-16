---
name: final-output
description: Master end-to-end dissertation pipeline orchestrator coordinating research staging, biology logic, chapter drafting, citation verification, Reviewer 2 audit, stylistic scan, and LaTeX publication build.
---

# Final Output: Master Dissertation Pipeline Orchestrator

The `final-output` skill coordinates the research, verification, and publication workflow for this Biology & Zoology dissertation. It unifies the six project skills into an auditable 7-stage pipeline.

## Overview & Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Master Dissertation Pipeline                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. STAGING           : Ingest drafts, notes, papers, citations              │
│                        (bio-research-sources)                               │
│ 2. BIOLOGY LOGIC     : Validate nomenclature, ethics notes & taxon macros   │
│                        (bio-nomenclature-ethics)                            │
│ 3. CHAPTER DRAFTING  : Scaffold & verify chapters, appendices, figures      │
│                        (bio-chapter-builder)                                │
│ 4. CITATION AUDIT    : Resolve BibLaTeX keys, deduplicate, check coverage   │
│                        (bio-reference-manager)                              │
│ 5. ADVERSARIAL REVIEW: Claim audit and methodology critique                 │
│ 6. DE-AI & HUMANIZE  : Scan prose for promotional fluff and AI tells        │
│ 7. FINAL BUILD       : Headless Tectonic compile to dissertation.pdf        │
│                        (build.py, verify.py -> 0 broken refs, 0 [?])        │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Run the Full End-to-End Pipeline
```bash
uv run python pipeline.py --all
```
This executes all 7 stages sequentially, writing structured checkpoints and audit reports into `pipeline_outputs/` and compiling `dissertation.pdf`.

### 2. Inspect Pipeline State & Available Stages
```bash
# List all stages
uv run python pipeline.py --list-stages

# View current pipeline execution status
uv run python pipeline.py --status

# Audit the 6 dissertation skills
uv run python pipeline.py --audit-skills
```

### 3. Run an Individual Pipeline Stage
```bash
uv run python pipeline.py --stage adversarial_review
uv run python pipeline.py --stage de_ai_humanizer
uv run python pipeline.py --stage final_build
```

### 4. Run via Skill Wrapper CLI
```bash
uv run python .agents/skills/final-output/scripts/run_pipeline.py --all
uv run python .agents/skills/final-output/scripts/run_pipeline.py --audit-skills
```

## Stage Inventory & Artifact Outputs

| Stage | Name | Key Skills | Generated Deliverables |
|:---|:---|:---|:---|
| **1** | `staging` | `bio-research-sources` | `pipeline_outputs/sources_manifest.json`, `pipeline_outputs/skills_inventory.json` |
| **2** | `biology_logic` | `bio-nomenclature-ethics` | `pipeline_outputs/biology_logic_audit.json` |
| **3** | `chapter_drafting` | `bio-chapter-builder` | `pipeline_outputs/drafting_status.json` |
| **4** | `citation_audit` | `bio-reference-manager` | `pipeline_outputs/citation_verification.json` |
| **5** | `adversarial_review` | pipeline heuristics | `pipeline_outputs/reviewer2_audit.md` |
| **6** | `de_ai_humanizer` | pipeline heuristics | `pipeline_outputs/de_ai_humanizer_report.md` |
| **7** | `final_build` | `build.py`, `verify.py` | `dissertation.pdf`, `pipeline_outputs/final_verification_report.json` |

## Pipeline State & Checkpoint Data Contract

Execution checkpoints are recorded in `pipeline_outputs/pipeline_state.json`:
```json
{
  "last_run": "2026-09-17T00:00:00Z",
  "stages": {
    "staging": {"status": "SUCCESS"},
    "biology_logic": {"status": "SUCCESS"},
    "chapter_drafting": {"status": "SUCCESS"},
    "citation_audit": {"status": "SUCCESS"},
    "adversarial_review": {"status": "SUCCESS", "report": "reviewer2_audit.md"},
    "de_ai_humanizer": {"status": "SUCCESS", "report": "de_ai_humanizer_report.md"},
    "final_build": {"status": "SUCCESS", "pdf": "dissertation.pdf"}
  },
  "overall_status": "COMPLETED"
}
```

## References

- `references/pipeline_architecture.md`: Stage-by-stage architecture, schemas, and error recovery.
- `examples/pipeline_run_example.md`: Example walkthrough for full pipeline execution.
