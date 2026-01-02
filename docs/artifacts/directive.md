# Micro-Claims Tracker — Directive

## Scope contract
This repo implements a single-user, local-only web app that captures micro-claims, supports triage/resolution, and exports a deterministic weekly digest. MVP must remain lean: no auth, no integrations, no LAN mode, no packaging, no configurable types.

## Stack (frozen)
- Backend: FastAPI
- Templates: Jinja (server-rendered)
- DB: SQLite
- Minimal JavaScript only for:
  - claim_uuid generation
  - disabling submit while saving
  - copy-to-clipboard (with fallback)

## Frozen domain rules
### Status model
- Allowed statuses: Open → In Review → Resolved
- No delete; no rejected status

### Editing model
- Type locked after create
- Editable: description, severity
- Always editable: status, resolved_note

### Time model
- created_at set once on create
- updated_at set on any update
- resolved_at:
  - set when status becomes Resolved
  - cleared if status moves out of Resolved
- “Weekly” semantics: Monday-start, local time
- Export uses explicit date ranges (UI may include shortcuts)

### De-dupe model
- claim_uuid generated client-side and submitted with create
- server enforces uniqueness and returns a safe “already captured” response for duplicates
- submit button disabled while saving

### Attachment model
- 0–1 photo per claim
- max 5MB
- stored on disk under data directory (uploads/)
- update with new photo overwrites old, and missing file is non-fatal (“photo missing”)

### Noise handling without Rejected
- resolution_outcome is set on resolve: valid or invalid
- use invalid to mark noise without changing status model

## Data directory (frozen default)
- Use OS-appropriate app data directory
- Default path on *nix: `~/.claims_tracker/`
- Must display the resolved data path in UI with a one-line manual backup instruction

## Export format (frozen)
- Deterministic: same inputs → same output
- Include:
  - from/to date range
  - generated timestamp
  - counts by type/severity/status
  - stable ordering: created_at DESC
- Outputs:
  - download .md
  - copy-to-clipboard (fallback to selectable textarea)

## Routes (recommended defaults; change only if needed)
Assumption: server-rendered pages can be implemented as:
- GET /  (dashboard list + filters)
- GET /claims/new
- POST /claims
- GET /claims/{id}
- POST /claims/{id}/update  (allowed edits)
- POST /claims/{id}/status  (status changes + resolve fields)
- POST /export  (returns digest)
If routes differ, update this directive to match (do not invent extra features).

## Verification definition (MVP)
Manual checklist must pass:
- Create claim <30s; no duplicates on double-click
- Resolve sets resolved_at; moving out clears it
- Search/filter returns correct rows
- Export is deterministic and correct for date range / Monday semantics
- Data folder path visible; backup instruction present
- Missing photo file is non-fatal and labeled

## Explicit non-goals (MVP)
- LAN mode / phone capture
- multi-user, auth, RBAC
- assignment/comments/notifications
- analytics/hotspots/cost estimates
- integrations (Sheets/Slack/WQT/WMS)
- configurable claim types/settings
- packaging/installer
- full event sourcing
