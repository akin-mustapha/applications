---
name: Business Requirements
---

# Business Requirements

## Problem Statement

`USER` is an AI Engineer writing many prompt markdown files and struggles to keep track of them — finding, reusing, and managing templates across projects is painful. This app solves that with a local, single-user prompt management tool.

## Goals & Success Metrics

- User can find any prompt in under 10 seconds via search
- User can create a reusable template with variable placeholders and instantiate prompts from it
- User can export any prompt in `.md`, `.yaml`, or `.json` format
- All data is stored locally — no external dependencies beyond Docker

## Stakeholders & Users

**Primary user:** AI Engineer creating and managing prompt files locally

## Constraints & Assumptions

- Single user, local only
- No authentication
- No caching layer
- No cloud dependency
- No edit history (future dev)
- Docker required for MongoDB

## Future Dev

- Prompt Testing Feature — run a prompt against an LLM and inspect output
- Edit history / versioning
- Auth + multi-user support
- Tag management UI (view all tags, rename, merge)
- Cloud storage option
