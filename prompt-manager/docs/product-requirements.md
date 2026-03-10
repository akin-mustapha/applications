---
name: Product Requirements
---

# Product Requirements

Prompt Manager is a single-page application that allows `USER` to manage prompts and templates locally.

## User Stories

### Prompt Stories

- As a user, I want to create a prompt so that I can store and access it later
- As a user, I want to create a prompt from a template so that I can reuse a defined structure
- As a user, I want to add free-form tags to a prompt so that I can organise and filter them
- As a user, I want to search prompts by name, description, and content so that I can quickly find what I need
- As a user, I want to export a prompt to `.md`, `.yaml`, or `.json` so that I can use it in other tools

### Template Stories

- As a user, I want to create a template with variable placeholders so that I can guide prompt creation consistently
- As a user, I want each variable in a template to have a name and description so I know what to fill in
- As a user, I want to search templates by name and description so that I can find the right starting point

---

## Functional Requirements

### Prompts

#### Fields

| Field              | Type          | Notes                                      |
|--------------------|---------------|--------------------------------------------|
| `id`               | string (UUID) | Auto-generated                             |
| `name`             | string        | Required                                   |
| `description`      | string        | Optional                                   |
| `content`          | string        | Markdown body                              |
| `tags`             | string[]      | Free-form, multiple allowed                |
| `template_id`      | string (ref)  | Optional — set if created from a template  |
| `variable_values`  | map[str, str] | Filled variable values if from a template  |
| `created_datetime` | datetime      | Auto-set on creation                       |
| `updated_datetime` | datetime      | Auto-updated on edit                       |

#### Features

- **Markdown support** — content field is written and stored as markdown
- **Edit + Preview split** — left half is the raw markdown editor, right half is live preview
- **Tagging** — free-form tags, multiple per prompt
- **Search** — full-text search across `name`, `description`, and `content`
- **Create from template** — user selects a template, fills in variable values (guided by variable descriptions), prompt content is generated with placeholders replaced
- **Export** — export any prompt to `.md`, `.yaml`, or `.json`

---

### Templates

#### Fields

| Field              | Type          | Notes                                          |
|--------------------|---------------|------------------------------------------------|
| `id`               | string (UUID) | Auto-generated                                 |
| `name`             | string        | Required                                       |
| `description`      | string        | Optional                                       |
| `content`          | string        | Markdown with `{{variable_name}}` placeholders |
| `variables`        | Variable[]    | List of variable definitions (see below)       |
| `created_datetime` | datetime      | Auto-set on creation                           |
| `updated_datetime` | datetime      | Auto-updated on edit                           |

#### Variable Definition

| Field         | Type   | Notes                                                       |
|---------------|--------|-------------------------------------------------------------|
| `name`        | string | Matches placeholder in content, e.g. `role` for `{{role}}` |
| `description` | string | Shown to user when filling in the value                     |

#### Features

- **Markdown support** — content supports `{{variable_name}}` placeholders
- **Variable guidance** — when instantiating a prompt from a template, each variable is presented with its name and description so the user knows what to enter
- **Search** — search by `name` and `description`
- No tagging on templates

---

## Non-Functional Requirements

- Local-only: all data stored in a Docker-hosted MongoDB instance
- No login or auth required
- Export must produce valid, clean `.md`, `.yaml`, and `.json` files
- App should be runnable with a single `docker-compose up` command

---

## UI Layout

Three-pane layout:

```text
+------------------------------------------+------------------+
|                                          |                  |
|         CENTER: Editor (split)           |  RIGHT SIDEBAR   |
|   [Markdown Editor] | [Live Preview]     |                  |
|                                          |  - Prompt list   |
|                                          |  - Template list |
|                                          |  - Search bar    |
+------------------------------------------+  - New buttons   |
|                                          |                  |
|         BOTTOM PANE                      +------------------+
|                                          |
|  - Metadata: name, description, tags     |
|  - Template variable input form          |
|    (shown when creating from template)   |
|  - Export controls                       |
+------------------------------------------+
```

- **Center pane:** split-view markdown editor (left) and live preview (right)
- **Bottom pane:** metadata fields (name, description, tags), template variable input when applicable, and export actions
- **Right sidebar:** navigation — lists prompts and templates, search bar, and buttons to create new prompt or template
