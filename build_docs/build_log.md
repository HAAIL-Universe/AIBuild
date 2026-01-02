# Build Log

## [2026-01-01 12:00:00] Greenfield MVP Build

**Objective:** Implement Micro-Claims Tracker MVP based on frozen directive.

**Evidence Summary:**
- Repo tree confirmed (build_docs/, contracts/, README.md present).
- Python 3.12.3 available.
- No existing app code found.

**Root-Cause Anchors:**
- Greenfield build (N/A)

**Patch Summary:**
- Created `requirements.txt`
- Created `main.py` (FastAPI entry point)
- Created `claims/` module (`models.py`, `db.py`, `repo.py`, `storage.py`, `export.py`)
- Created `templates/` (`base.html`, `index.html`, `new_claim.html`, `claim_detail.html`)
- Created `static/` (`styles.css`, `app.js`)

**Verification Results:**
1.  **Static Correctness:**
    - All files created with correct imports.
    - No syntax errors detected during creation.
2.  **Runtime Sanity:**
    - `uvicorn main:app --reload` started successfully.
    - `TestClient` verification passed for all endpoints.
3.  **Behavioral Intent:**
    - **Static Assets**: `/static/styles.css` and `/static/app.js` load (200 OK).
    - **App Init**: Root endpoint `/` returns 200 OK.
    - **Create Claim**: POST `/claims` persists to DB and redirects.
    - **Duplicate Prevention**: Re-submitting same UUID redirects to existing claim (safe idempotency).
    - **Status Workflow**: Open -> In Review -> Resolved (sets `resolved_at`) -> Open (clears `resolved_at`).
    - **Export**: Generates markdown digest with correct content.
4.  **Contract Compliance:**
    - Scope respected (Local-only, SQLite, Jinja).
    - Data directory logic implements OS-appropriate paths.
    - Deterministic export logic implemented.

**Stop Reason:**
- N/A (Completed)

## [2026-01-01 14:00:00] Verification & Hardening

**Objective:** Close evidence gaps and apply minimal patches for contract compliance.

**Patch Summary:**
- `main.py`: Enforced 5MB upload size limit (HTTP 413).
- `templates/index.html`: Added data folder path and backup guidance.
- `claims/export.py`: Removed seconds from generation timestamp for determinism.

**Verification Results:**
1.  **UI Boot:** Verified static assets, app init, and data path display.
2.  **Dedupe:** Verified DB uniqueness and safe redirect on double-submit.
3.  **Resolved Semantics:** Verified `resolved_at` set/clear logic in DB.
4.  **Export:** Verified identical output for repeated runs on same date range.
5.  **Missing Photo:** Verified `onerror` handler presence in HTML.

**Stop Reason:**
- Verification Complete.

## [2026-01-02 09:00:00] Compliance & Polish

**Objective:** Bring repo into full compliance with blueprint/directive (Filters, Export Headers, Logging).

**Patch Summary:**
- `main.py`: Added logging, Type/Date filters, Export headers, Photo cleanup logic.
- `templates/index.html`: Added Type filter and Date range inputs.
- `static/app.js`: Added clipboard fallback modal.
- `claims/storage.py`: Added `delete_upload` utility.
- `README.md`: Updated data path documentation.
- `.gitignore`: Added standard Python/Project ignores.

**Verification Results:**
1.  **Filters:** Verified Type and Date filters pass correctly to repo.
2.  **Export:** Verified `.md` download with correct filename and headers.
3.  **Clipboard:** Verified fallback modal appears when clipboard API fails (simulated).
4.  **Observability:** Verified `app.log` creation in data directory.
5.  **Lifecycle:** Verified old photos are deleted on update.

**Stop Reason:**
- Compliance Complete.

## [2026-01-02 10:00:00] Repo Hygiene & Release Polish

**Objective:** Repo hygiene + release polish

**Patch Summary:**
- `.gitignore`: Added ignores for logs, DBs, and test outputs.
- `README.md`: Added explicit "Run" and "Verify" sections.
- Cleanup: Removed runtime artifacts (`server.log`, `test_output.txt`, etc.).

**Verification Results:**
1.  **Static Correctness:** `.gitignore` includes all runtime artifacts.
2.  **Runtime Sanity:** Server starts cleanly.
3.  **Behavioral Intent:** Verification script passes all checks.
4.  **Contract Compliance:** No scope creep; local-only maintained.

**Stop Reason:**
- Compliance Complete

## [2026-01-02 11:00:00] v1.1 Hardening

**Objective:** v1.1 hardening (logging/determinism/indexes/migration guard)

**Patch Summary:**
- `main.py`: Implemented named logger with handler deduplication for reload safety.
- `claims/db.py`: Added SQLite indexes and `user_version` migration guard.
- `claims/export.py`: Enforced ISO date formatting and stable generation timestamp.
- `verify_compliance.py`: Added checks for logging, indexes, and determinism.

**Verification Results:**
1.  **Static Correctness:** Logger config uses `getLogger` and checks handlers.
2.  **Runtime Sanity:** Server starts, reloads without duplicate logs.
3.  **Behavioral Intent:** Exports are deterministic (ISO dates). Indexes exist.
4.  **Contract Compliance:** No scope creep; no new features.

**Stop Reason:**
- Hardening Complete.

## [2026-01-02 12:00:00] Self-Hosting Packaging

**Objective:** Add SELF_HOSTING guide + README link (+ optional CLAIMS_DATA_DIR override)

**Patch Summary:**
- `docs/SELF_HOSTING.md`: Added guide for Local, LAN, and Cloud hosting.
- `README.md`: Added Self-Hosting section and safety warning.
- `claims/storage.py`: Added `CLAIMS_DATA_DIR` env var support for custom persistence.

**Verification Results:**
1.  **Static Correctness:** Docs link works, env var logic handles overrides correctly.
2.  **Runtime Sanity:** Server starts normally.
3.  **Behavioral Intent:** Setting `CLAIMS_DATA_DIR` redirects DB/uploads to new path.
4.  **Contract Compliance:** No auth added, no schema changes.

**Stop Reason:**
- Packaging Complete.

## [2026-01-02 13:00:00] Business-Trial Posture

**Objective:** Business-trial posture + optional Basic Auth + docs alignment

**Patch Summary:**
- `main.py`: Added optional Basic Auth (env-gated) using `secrets.compare_digest`.
- `SECURITY.md`: Updated deployment models to include Cloud Self-Host with Auth.
- `docs/SELF_HOSTING.md`: Prioritized Local/Cloud options, added Auth config.
- `README.md`: Added Trial Modes section.
- `verify_compliance.py`: Added auth logic test (default state).

**Verification Results:**
1.  **Static Correctness:** Auth logic uses constant-time comparison.
2.  **Runtime Sanity:** Server starts with/without auth env vars.
3.  **Behavioral Intent:** Default run remains unauthenticated.
4.  **Contract Compliance:** No new dependencies, no schema changes.

**Stop Reason:**
- Posture Complete.
