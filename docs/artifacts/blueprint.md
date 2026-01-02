# Micro-Claims Tracker — Blueprint

## One-liner
A local-first micro-claims log that captures small warehouse issues in seconds, makes them searchable, and exports a deterministic weekly digest so they stop vanishing.

## Problem
Small losses and issues (damaged stock, missing kit, short picks, unsafe locations, supplier faults) don’t get logged properly → they vanish → nobody learns → cost repeats.

## MVP success loop (definition of “done”)
Capture → triage → resolve → retrieve → weekly digest, in one local web app.

### Measurable targets
- Create claim end-to-end in **< 30 seconds**
- Find/filter claim in **< 10 seconds**
- Export weekly digest in **< 5 seconds**
- Search/filter returns in **< 300ms** for up to **~5k claims** locally

## Hard constraints
- Local-only (localhost), **single user**, **no auth**, **no integrations**
- Minimal moving parts: **FastAPI + Jinja + SQLite**, minimal JavaScript
- Any destructive action (delete) is not in MVP
- Deterministic build loop (for future implementation): evidence-first, minimal diff, verify in order

## Core entities
### Claim (frozen MVP schema)
| Field | Type | Notes |
|---|---|---|
| id | int pk | auto |
| claim_uuid | text unique | client-generated; server de-dupe |
| created_at | datetime | set on create |
| updated_at | datetime | set on update |
| resolved_at | datetime nullable | set/cleared deterministically on status change |
| type | text enum | Damage / Shortage / Missing Kit / Safety / Other |
| severity | text enum | Low / Med / High |
| status | text enum | Open / In Review / Resolved |
| description | text | required |
| resolved_note | text nullable | editable |
| resolution_outcome | text enum nullable | valid / invalid (set on resolve) |
| photo_path | text nullable | 0–1 attachment |

## Trust guardrails (frozen into MVP)
### Mandatory (MVP)
1) **Time semantics:** store `created_at` and `resolved_at` on Claim (nullable).
2) **Duplicate prevention:** client-generated `claim_uuid` + disable submit while saving + server de-dupe.
3) **Backup visibility:** show data folder path prominently in UI with one-line manual backup instruction.

### Small add-ons (MVP)
4) **Noise handling without Rejected:** `resolution_outcome = valid|invalid` set on resolve (no extra status).
5) **Attachment lifecycle:** overwrite/delete old photo on replace; handle missing files gracefully (“photo missing”).
6) **Deterministic export:** same inputs → same output; include date range + generated timestamp + stable ordering.

### Optional (bounded, MVP)
7) **Fast filtering UX:** exactly 3 preset buttons: Open only / High severity / This week.

## UI surfaces and core flows
### MVP UI surface
- Single local web app (responsive enough for desktop demo; no LAN/mobile requirement)

### Core flows (must-have)
1) **Create claim**
   - type, severity, description, optional photo (0–1), save as Open
2) **Triage + update**
   - status transitions: Open ↔ In Review → Resolved
   - resolved note + (on resolve) resolution_outcome valid/invalid
3) **Find + export**
   - filters (type/status/severity/date range) + search (description + resolved_note)
   - weekly digest export: download + copy-to-clipboard

## Editing policy (MVP)
- Type: **locked after creation**
- Editable: **description, severity**
- Always editable: **status, resolved_note** (with deterministic `resolved_at` behavior)
- Delete: **not in MVP**

## Data + storage rules (MVP)
- Source of truth: SQLite DB stored under OS-appropriate app data directory:
  - default: `~/.claims_tracker/` (or platform equivalent)
- Uploads stored on disk under the same data folder (e.g., `uploads/`)
- Store only `photo_path` in DB
- Photo size limit: **5MB**
- Missing photo files must not break list/detail views

## Export rules (MVP)
- Monday-start, local time semantics for “weekly”
- Export is by explicit date range (with shortcut buttons allowed as UI sugar)
- Export content (fixed format):
  - date range
  - generated timestamp
  - counts by type/severity/status
  - stable ordered list (freeze ordering: `created_at DESC`)
- Export outputs:
  - download `.md` (optional `.txt` if trivial)
  - copy-to-clipboard (fallback to selectable textarea if permissions fail)

## Observability (MVP)
- Local log file (e.g., `app.log`) capturing:
  - errors
  - key actions: created, status change, export generated

## Testing / verification (MVP)
Manual checklist:
- Create claim <30s; no duplicates on double-click
- Resolve sets `resolved_at`; moving out of Resolved clears it
- Search/filter returns correct rows
- Export matches deterministic format and correct date slicing
- Data path visible; backup instruction present
- Missing photo file is non-fatal and labeled

## Phase 2+ (explicitly deferred)
- LAN mode / phone capture
- Multi-user + roles/RBAC + auth
- Assignment/comments/notifications
- Zip backup download + restore
- Analytics/hotspots/cost estimate
- WQT/WMS integration fields + imports
- Configurable claim types/settings
- Packaging (double-click install)
- Full event sourcing / advanced audit trails

## High-level layout (minimal)
- One “Dashboard” page
  - Header: New Claim button
  - Filters: type/status/severity/date range + search
  - Presets row (optional): Open only | High severity | This week
  - Main list/table: claims with quick status update + view/edit
  - Claim detail (modal or page): allowed edits + resolve (note + outcome) + photo
  - Export section: range selector + Download + Copy
  - Footer/settings-lite: data folder path + backup one-liner
