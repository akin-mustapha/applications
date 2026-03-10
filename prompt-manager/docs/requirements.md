---
name: Requirements
---

# Overview

## Business Requirements

### Problem Statement

`USER` has been writing a lot of prompt md files. User finds it hard to keep track of these files, the templates and history.

### Goal & Success Metrics

### Stakeholders & Users

**Primary user:** AI Engineer creating prompt files

### Constraints & Assumptions

- Single User
- Local
- No Cloud dependency
- No support for edit history (future dev)

## Product Requirements

Prompt Manager, a single page application that allows `USER` to:

- Manage prompts (create, update, delete, view)
- Manage templates (create, update, delete, view)

### User Stories

- As a user, I want to create a prompt document, so that I can access it later
- As a user, I want to create a template for my prompt, so that I can reuse template across different projects.

---

### Functional Requirements

#### Prompts

##### Features

- Markdown Support
- Tagging
- Search/Filter

##### Fields

- name
- description
- content
- created_datetime
- updated_datetime

---

#### Templates

##### Features

- Markdown Support
- Search/Filter

##### Fields

- name
- description
- content
- created_datetime
- updated_datetime

**History:**

**Search:**

## Architecture

**Frontend:** Single Page User Interface

- React or Dash (maybe a Dash prototype)

**Service:**

- Fast API or Django
- API
- Cache (later)
- Auth (later)

  **Components**
  - Entities: Template, Prompt
  - Use Cases

**Storage:**

- MongoDB
  - local or docker
  - schema

## Future Dev

- Prompt Testing Feature
