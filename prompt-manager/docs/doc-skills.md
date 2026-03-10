---
name: Skills
description: Documentation on project skills
---

# Skills

Custom Claude Code skills for the Prompt Manager project. Each skill pre-loads the relevant docs and enforces a specific role and workflow.

## Structure

```txt
.claude/skills/
├── pm/SKILL.md          → /pm
├── architect/SKILL.md   → /architect
├── build/SKILL.md       → /build
└── bug-hunter/SKILL.md  → /bug-hunter
```

## Skills Overview

| Skill | Role | Key Docs | Decision Authority |
|---|---|---|---|
| `/pm` | Scope & task breakdown | `business-requirements.md`, `product-requirements.md` | None — flags to human |
| `/architect` | Design & data model review | `architecture.md`, `product-requirements.md` | Proposes, human confirms |
| `/build` | Feature implementation | `architecture.md`, `CLAUDE.md` | Implements only what's asked |
| `/bug-hunter` | Debug + log to `docs/bugs.md` | `architecture.md`, `bugs.md` | Fix root cause only |

## Notable Behaviours

- `/bug-hunter` creates `docs/bugs.md` on first use and appends a structured entry on every subsequent bug — building a persistent diagnostic history
- `/architect` is hardwired to ask before deciding — mirrors the CLAUDE.md implementer rule
- `/build` is configured to stop and defer to `/architect` if it encounters a design decision during implementation
