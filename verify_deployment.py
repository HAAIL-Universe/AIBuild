import sys
import time
import urllib.request
import urllib.parse
import json
import sqlite3
import uuid
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"

def log(msg):
    print(f"[TEST] {msg}")

def wait_for_server():
    for i in range(10):
        try:
            urllib.request.urlopen(BASE_URL)
            log("Server is up.")
            return
        except:
            time.sleep(1)
    log("Server failed to start.")
    sys.exit(1)

def test_ui_boot():
    log("--- 2A. UI Boot Proof ---")
    # Static assets
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/static/styles.css")
        assert resp.status == 200
        log("PASS: Static assets load (/static/styles.css)")
    except Exception as e:
        log(f"FAIL: Static assets: {e}")

    # App initializes
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/")
        assert resp.status == 200
        content = resp.read().decode()
        log("PASS: App initializes (GET / 200 OK)")
        
        if "Data Location:" in content:
             log("PASS: Data folder path shown on dashboard")
        else:
             log("FAIL: Data folder path NOT shown")
             
    except Exception as e:
        log(f"FAIL: App init: {e}")

def create_claim_request(claim_uuid, description="Test Claim", with_photo=False):
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    data = []
    data.append(f'--{boundary}')
    data.append('Content-Disposition: form-data; name="claim_uuid"')
    data.append('')
    data.append(claim_uuid)
    data.append(f'--{boundary}')
    data.append('Content-Disposition: form-data; name="type"')
    data.append('')
    data.append('Other')
    data.append(f'--{boundary}')
    data.append('Content-Disposition: form-data; name="severity"')
    data.append('')
    data.append('Low')
    data.append(f'--{boundary}')
    data.append('Content-Disposition: form-data; name="description"')
    data.append('')
    data.append(description)
    
    if with_photo:
        data.append(f'--{boundary}')
        data.append('Content-Disposition: form-data; name="photo"; filename="test.jpg"')
        data.append('Content-Type: image/jpeg')
        data.append('')
        data.append('fakeimagecontent')
        
    data.append(f'--{boundary}--')
    data.append('')
    
    body = '\r\n'.join(data).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/claims", data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    return req

def test_dedupe():
    log("--- 2B. Double-submit De-dupe Proof ---")
    claim_uuid = str(uuid.uuid4())
    
    # First submit
    req = create_claim_request(claim_uuid)
    try:
        resp = urllib.request.urlopen(req)
        log(f"PASS: First submit successful. URL: {resp.geturl()}")
        first_url = resp.geturl()
    except Exception as e:
        log(f"FAIL: First submit failed: {e}")
        return

    # Second submit
    req2 = create_claim_request(claim_uuid)
    try:
        resp2 = urllib.request.urlopen(req2)
        log(f"PASS: Second submit handled safely. URL: {resp2.geturl()}")
        if resp2.geturl() == first_url:
            log("PASS: Redirected to same claim URL.")
        else:
            log(f"WARN: Redirected to different URL? {resp2.geturl()}")
    except urllib.error.HTTPError as e:
        log(f"FAIL: Second submit crashed with {e.code}")
    except Exception as e:
        log(f"FAIL: Second submit error: {e}")

    # Check DB count
    # Get data dir dynamically
    if os.name == 'nt':
        base_dir = os.getenv('APPDATA')
    else:
        base_dir = os.path.expanduser('~')
    db_path = os.path.join(base_dir, ".claims_tracker", "claims.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM claims WHERE claim_uuid = ?", (claim_uuid,))
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 1:
        log(f"PASS: DB row count is 1 for UUID {claim_uuid}")
    else:
        log(f"FAIL: DB row count is {count}")

def test_resolved_at():
    log("--- 2C. resolved_at Semantics Proof ---")
    # Create a claim to test
    claim_uuid = str(uuid.uuid4())
    req = create_claim_request(claim_uuid, "Resolve Test")
    resp = urllib.request.urlopen(req)
    claim_url = resp.geturl()
    claim_id = claim_url.split('/')[-1]
    
    # Resolve it
    data = urllib.parse.urlencode({
        'status': 'Resolved',
        'resolution_outcome': 'Valid',
        'resolved_note': 'Fixed'
    }).encode()
    req_resolve = urllib.request.Request(f"{BASE_URL}/claims/{claim_id}/status", data=data)
    urllib.request.urlopen(req_resolve)
    
    # Check DB
    if os.name == 'nt':
        base_dir = os.getenv('APPDATA')
    else:
        base_dir = os.path.expanduser('~')
    db_path = os.path.join(base_dir, ".claims_tracker", "claims.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT resolved_at FROM claims WHERE id = ?", (claim_id,))
    resolved_at = cursor.fetchone()[0]
    if resolved_at:
        log(f"PASS: resolved_at set to {resolved_at}")
    else:
        log("FAIL: resolved_at is NULL after resolving")
        
    # Un-resolve it
    data = urllib.parse.urlencode({
        'status': 'Open'
    }).encode()
    req_open = urllib.request.Request(f"{BASE_URL}/claims/{claim_id}/status", data=data)
    urllib.request.urlopen(req_open)
    
    cursor.execute("SELECT resolved_at FROM claims WHERE id = ?", (claim_id,))
    resolved_at_new = cursor.fetchone()[0]
    conn.close()
    
    if resolved_at_new is None:
        log("PASS: resolved_at cleared (NULL) after reopening")
    else:
        log(f"FAIL: resolved_at is {resolved_at_new} after reopening")

def test_export_determinism():
    log("--- 2D. Export Determinism Proof ---")
    today = datetime.now().strftime('%Y-%m-%d')
    data = urllib.parse.urlencode({
        'date_from': today,
        'date_to': today
    }).encode()
    
    req = urllib.request.Request(f"{BASE_URL}/export", data=data)
    
    resp1 = urllib.request.urlopen(req).read()
    resp2 = urllib.request.urlopen(req).read()
    
    if resp1 == resp2:
        log("PASS: Export outputs are identical")
        # log(f"Snippet: {resp1[:50]}...")
    else:
        log("FAIL: Export outputs differ")

def test_missing_photo():
    log("--- Extra: Missing Photo Proof ---")
    claim_uuid = str(uuid.uuid4())
    # Create with photo so the IMG tag is rendered
    req = create_claim_request(claim_uuid, "Photo Test", with_photo=True)
    resp = urllib.request.urlopen(req)
    
    content = resp.read().decode()
    if "onerror" in content:
        log("PASS: Detail page has onerror handler for missing photo")
    else:
        log("WARN: Could not verify missing photo handling (onerror not found)")

if __name__ == "__main__":
    wait_for_server()
    test_ui_boot()
    test_dedupe()
    test_resolved_at()
    test_export_determinism()
    test_missing_photo()
