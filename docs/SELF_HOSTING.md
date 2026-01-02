# Self-Hosting Guide

This application is designed as a local-first trial tool, but it can be self-hosted on your own infrastructure for team use.

**WARNING: No Authentication**
By default, this application has **NO** authentication.
- **Do not** deploy it to the public internet without enabling Basic Auth (see below) or using a VPN.
- **Do not** store sensitive PII or HIPAA-regulated data.

**Distribution Note:**
If you downloaded a zip that contains a `.git` folder, delete it; use GitHub "Download ZIP" instead to ensure a clean start.

---

## Option 1: Local PC Trial (Recommended)

The simplest way to run the tracker is on your own machine.

### Windows (PowerShell)
1.  **Install Python 3.12+** (Check "Add Python to PATH")
2.  **Setup:**
    ```powershell
    python -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt
    ```
3.  **Run:**
    ```powershell
    .venv\Scripts\python -m uvicorn main:app --reload --port 8000
    ```
4.  **Access:** `http://localhost:8000`
    *Data Location: `%APPDATA%\.claims_tracker`*

### macOS / Linux
1.  **Setup:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Run:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```
3.  **Access:** `http://localhost:8000`
    *Data Location: `~/.claims_tracker`*

---

## Option 2: Cloud Self-Hosting (Your Account)

Deploy to a cloud provider (Render, Railway, etc.) for mobile access.

**Configuration:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Persistence (Critical):**
1.  Attach a persistent disk (mount at `/var/data`).
2.  Set Env Var: `CLAIMS_DATA_DIR=/var/data/claims_tracker`.

**Security (Basic Auth):**
To protect your deployment, set these environment variables:
- `BASIC_AUTH_USER=admin`
- `BASIC_AUTH_PASS=your-secure-password`

*The app will prompt for these credentials before allowing access.*

---

## Option 3: LAN Run (Advanced)

To share on a trusted internal Wi-Fi/LAN.

1.  Find your local IP (e.g., `192.168.1.50`).
2.  Run listening on all interfaces:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
3.  Access via `http://192.168.1.50:8000`.

*Note: Anyone on the network can edit data. Use only on trusted networks.*

---

## Verification & Backups

**Verify Installation:**
Run `python verify_compliance.py`. All tests should pass.

**Backups:**
Copy the contents of the data directory (`claims.db`, `uploads/`, `app.log`).
To restore, stop the server and replace the files.
