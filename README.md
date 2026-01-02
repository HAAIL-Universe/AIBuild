# Micro-Claims Tracker

A local-first micro-claims log that captures small warehouse issues in seconds, makes them searchable, and exports a deterministic weekly digest so they stop vanishing.

## Problem
Small losses and issues (damaged stock, missing kit, short picks, unsafe locations, supplier faults) don’t get logged properly because the process is too heavy. They vanish, nobody learns, and the cost repeats.

## MVP Scope Boundaries
This is a strict MVP with hard constraints:
- **Local-only**: Runs on localhost.
- **Single User**: No authentication, no multi-user support.
- **No Integrations**: No connection to WMS, Slack, or email.
- **No LAN Mode**: Desktop use only.
- **No Delete**: Destructive actions are out of scope.

## Tech Stack
- **Backend**: FastAPI
- **Templates**: Jinja2 (server-rendered)
- **Database**: SQLite
- **Frontend**: Minimal JavaScript (no build pipeline)

## Quickstart

### Prerequisites
- Python 3.10+

### Run
1.  Create/Activate venv (optional):
    ```bash
    python -m venv .venv
    # Windows: .\.venv\Scripts\activate
    # Mac/Linux: source .venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start server:
    ```bash
    python -m uvicorn main:app --reload --port 8000
    ```
4.  Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Verify
Run the compliance suite to test routes, export headers, filters, determinism, and logging:
```bash
python verify_compliance.py
```

## Data & Backup
**Trust is paramount.** Your data is stored locally on your machine.

- **Location**: The application uses the OS-appropriate application data directory (e.g., `~/.claims_tracker/` on Linux/Mac, `%APPDATA%\.claims_tracker` on Windows).
- **Visibility**: The exact path is displayed prominently in the UI footer.
- **Backup**: To back up your data, simply copy the entire data folder to a safe location.
- **Photos**: Uploaded photos are stored in an `uploads/` subdirectory within the data folder.

## How to Use

### Core Flows
1.  **Create Claim (< 30s)**:
    - Select Type (Damage, Shortage, Missing Kit, Safety, Other).
    - Set Severity (Low, Med, High).
    - Enter Description.
    - (Optional) Upload one photo (Max 5MB).
    - **Note**: Type is locked after creation.

2.  **Triage & Update**:
    - Move status between **Open** ↔ **In Review** → **Resolved**.
    - Edit description or severity if needed.
    - **Duplicate Prevention**: The system prevents double-submissions.

3.  **Resolve**:
    - Set status to **Resolved**.
    - Add a **Resolved Note**.
    - Set **Resolution Outcome**: `Valid` or `Invalid` (for tracking noise without deleting).
    - *Note*: Moving a claim out of "Resolved" clears the resolution timestamp.

### Weekly Export
- **Semantics**: "Weekly" implies Monday-start, local time.
- **Format**: The export is deterministic (same inputs = same output).
- **Content**: Includes date range, generation timestamp, summary counts, and a stable ordered list of claims.
- **Output**: Download as Markdown or Copy to Clipboard.

## Definition of Done (Verification Checklist)
The following must be true for the system to be considered healthy:

- [ ] **No Duplicates**: Double-clicking submit does not create duplicate records.
- [ ] **Time Integrity**: `resolved_at` is set when Resolved, and cleared if reopened.
- [ ] **Search**: Filters and search return the correct rows.
- [ ] **Export**: Output is deterministic and respects the selected date range.
- [ ] **Data Safety**: Data folder path is visible in UI; backup instruction is present.
- [ ] **Resilience**: Missing photo files do not crash the application (labeled "photo missing").
