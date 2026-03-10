---
name: Project BRD
---

# Overview

## Business Requirement

`USER` has been writing a lot of prompt md files. User finds it hard to keep track of these files, the templates and history.

## Product Requirement

Prompt Manager, a single page application that allows `USER` to:

* Manage prompts (create, update, delete, view)
* Manage templates (create, update, delete, view)

## Architecture

**Frontend:** Single Page User Interface

* React or Dash (maybe a Dash prototype)

**Service:**

* Fast API or Django
* API
* Cache (later)
* Auth (later)

  **Components**
  * Entities: Template, Prompt
  * Use Cases

**Storage:**

* MongoDB
  * local or docker
  * schema

## Future Dev

* Prompt Testing Feature
