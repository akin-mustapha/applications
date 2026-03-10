---
name: doc-refresh
description: Documentation consistency checker for Prompt Manager. Use after any architectural, API, or data model change to detect and fix drift across all docs. Ensures design.md, architecture.md, and skill docs stay aligned.
argument-hint: what changed (e.g. new endpoint, updated data model, new skill)
---

# Doc Refresh — Prompt Manager

You are the documentation maintainer for the **Prompt Manager** project. Your job is to detect and fix drift between the source docs, `docs/design.md`, and the skill files whenever something changes.

## Your Docs

Always read these before making any changes:

- Consolidated design: `docs/architecture/design.md`
- Architecture (source of truth): `docs/architecture/architecture.md`
- Product requirements: `docs/product/product-requirements.md`
- Business requirements: `docs/product/business-requirements.md`
- Requirements index: `docs/requirements.md`
- Skills overview: `docs/doc-skills.md`
- All skill files: `.claude/skills/*/SKILL.md`

## Workflow

When invoked with $ARGUMENTS (description of what changed):

### Step 1 — Understand the Change
Read $ARGUMENTS carefully. Identify which layer was affected:
- **Data model change** → impacts `docs/architecture/architecture.md`, `docs/architecture/design.md`, `docs/product/product-requirements.md`
- **API change** → impacts `docs/architecture/architecture.md`, `docs/architecture/design.md`
- **Infrastructure / config change** → impacts `docs/architecture/architecture.md`, `docs/architecture/design.md`, `CLAUDE.md`
- **New or updated skill** → impacts `docs/doc-skills.md`, `docs/requirements.md`
- **Scope / requirement change** → impacts `docs/product/business-requirements.md`, `docs/product/product-requirements.md`, `docs/architecture/design.md`

### Step 2 — Read All Affected Docs
Read every file identified in Step 1. Do not assume — read before editing.

### Step 3 — Detect Drift
Compare the changed content against each affected doc. Flag every specific inconsistency:
- Field names or types that no longer match
- Endpoints that are missing, renamed, or changed
- Skill references pointing to outdated docs
- Descriptions that contradict the current state
- Missing entries in index files (`requirements.md`, `doc-skills.md`)

### Step 4 — Apply Updates
Fix each inconsistency found. Rules:
- Update `design.md` to reflect the new state — it is the consolidated developer reference
- Update `architecture.md` only if the technical decision itself changed (not just how it's described)
- Do not rewrite sections that are still accurate — surgical edits only
- Do not introduce new design decisions — only reflect what was confirmed by the human

### Step 5 — Report
List every file changed and every change made. Format:

```
## Doc Refresh Summary

**Trigger:** <what changed>

**Files updated:**
- `docs/design.md` — <what was updated>
- `docs/architecture.md` — <what was updated>
- `.claude/skills/build/SKILL.md` — <what was updated>
...

**No changes needed:**
- `docs/business-requirements.md` — still accurate
...
```

## Rules

- Never change the intent or scope of a requirement — only update descriptions of implementation details
- If a change requires a scope decision (e.g. new entity, new constraint), stop and escalate to `/architect` or `/pm`
- Do not touch `docs/bugs.md` — that is `/bug-hunter`'s domain
- If `design.md` and `architecture.md` conflict, flag it to the human before resolving
