---
name: Skills
description: Documentation on project skills
---

# Skills

Custom Claude Code skills for the Prompt Manager project. Each skill pre-loads the relevant docs and enforces a specific role and workflow.

## Structure

```txt
.claude/skills/
├── pm/SKILL.md           → /pm
├── architect/SKILL.md    → /architect
├── build/SKILL.md        → /build
├── bug-hunter/SKILL.md   → /bug-hunter
├── doc-refresh/SKILL.md  → /doc-refresh
└── gh-setup/SKILL.md     → /gh-setup
```

## Skills Overview

| Skill | Role | Key Docs | Decision Authority |
|---|---|---|---|
| `/pm` | Scope, task breakdown, iteration planning | `business-requirements.md`, `product-requirements.md` | None — flags to human |
| `/architect` | Design & data model review | `design.md`, `architecture.md`, `requirements.md` | Proposes, human confirms |
| `/build` | Feature implementation + phase planning | `design.md`, `requirements.md`, `CLAUDE.md` | Implements only what's asked |
| `/bug-hunter` | Debug + log to `docs/bugs.md` | `design.md`, `requirements.md`, `bugs.md` | Fix root cause only |
| `/doc-refresh` | Detect and fix doc drift after changes | All docs + all skill files | Updates descriptions only — escalates scope decisions |
| `/gh-setup` | Create GitHub iteration + phase issues | Approved pm + build plans | Creates issues only — never changes scope |

## Iteration Workflow

The standard workflow for planning and tracking a new implementation:

```
1. /pm iteration plan          → outputs structured iteration plan, pauses for approval
2. [Human approves]
3. /build phase plan iter N    → outputs phases for each iteration, pauses for approval
4. [Human approves]
5. /gh-setup all               → creates GitHub issues (parent per iteration, subissue per phase)
```

Each step requires explicit human sign-off before the next step proceeds.

## Notable Behaviours

- `/pm` now supports `iteration plan` mode — outputs a structured, numbered iteration plan and waits for approval before proceeding
- `/build` now supports `phase plan iteration N` mode — breaks an approved iteration into typed phases (setup, backend, frontend, test, integration) and waits for approval
- `/gh-setup` only runs after both plans are approved — creates parent iteration issues and phase subissues, links them, and reports a summary
- `/bug-hunter` creates `docs/bugs.md` on first use and appends a structured entry on every subsequent bug — building a persistent diagnostic history
- `/architect` is hardwired to ask before deciding — mirrors the CLAUDE.md implementer rule
- `/build` is configured to stop and defer to `/architect` if it encounters a design decision during implementation
- `/doc-refresh` is triggered by `/architect` after confirmed design decisions, and by `/build` after any implementation that changes an API contract or data model
