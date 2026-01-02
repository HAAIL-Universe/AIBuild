# Self-Hosting Guide

This application is designed as a local-first trial tool, but it can be self-hosted on your own infrastructure for team use.

**WARNING: No Authentication**
This application has **NO** built-in authentication or user management.
- **Do not** deploy it to the public internet without a VPN, firewall, or authentication proxy (like Authelia or Cloudflare Access).
- **Do not** store sensitive PII or HIPAA-regulated data.

**Distribution Note:**
If you downloaded a zip that contains a `.git` folder, delete it; use GitHub "Download ZIP" instead to ensure a clean start.

---

## A) Local Run — Windows

The simplest way to run the tracker is on your own machine using PowerShell.

1.  **Install Python 3.12+**
    Ensure "Add Python to PATH" is checked during installation.

2.  **Setup Virtual Environment:**
    ```powershell
    python -m venv .venv
    ```

3.  **Install Dependencies:**
    ```powershell
    .venv\Scripts\python -m pip install -r requirements.txt
    ```

4.  **Run the Server:**
    ```powershell
    .venv\Scripts\python -m uvicorn main:app --reload --port 8000
    ```

5.  **Access:** Open `http://localhost:8000`

**Data Location:** `%APPDATA%\.claims_tracker`

---

## B) Local Run — macOS / Linux

1.  **Install Python 3.12+**

2.  **Setup Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```

5.  **Access:** Open `http://localhost:8000`

**Data Location:** `~/.claims_tracker`

---

## C) LAN Run (Internal Network)

To share with colleagues on the same Wi-Fi/LAN. **Use on trusted networks only.**

1.  Find your computer's local IP address (e.g., `192.168.1.50`).
2.  Run the server listening on all interfaces:
    ```bash
    # Windows
    .venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8000
    
    # Mac/Linux
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
3.  Colleagues can access via `http://192.168.1.50:8000`.

*Note: Ensure your firewall allows traffic on port 8000.*

---

## D) Cloud Self-Hosting (e.g., Render, Railway)

You can deploy this to a cloud provider that supports Python.

**Configuration:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Persistence (Critical):**
By default, data is stored in the container's home directory, which is **ephemeral** (deleted on restart) on most cloud platforms.

To persist data, you must:
1.  Attach a persistent disk/volume to your service (e.g., mount at `/var/data`).
2.  Set the environment variable `CLAIMS_DATA_DIR` to that path.

**Example (Render.com):**
1.  Create a **Disk** named `claims-data` mounted at `/var/data`.
2.  Add Environment Variable: `CLAIMS_DATA_DIR=/var/data/claims_tracker`.

---

## E) Verification

To verify the installation is correct and compliant:

```bash
# Windows
.venv\Scripts\python verify_compliance.py

# Mac/Linux
python verify_compliance.py
```

All tests should pass.

---

## F) Backups

To back up your data, simply copy the contents of the data directory.

**What to back up:**
- `claims.db` (The SQLite database)
- `uploads/` (The photo directory)
- `app.log` (Application logs)

**Restoring:**
Stop the server, replace the files in the data directory, and restart.
