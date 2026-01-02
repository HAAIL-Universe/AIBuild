import sqlite3
from datetime import datetime
from typing import List, Optional
from .db import get_connection
from .models import Claim, ClaimCreate, ClaimUpdate, ClaimStatusUpdate, Status, ResolutionOutcome

class DuplicateClaimError(Exception):
    pass

def create_claim(claim: ClaimCreate, photo_path: Optional[str] = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    
    try:
        cursor.execute("""
            INSERT INTO claims (
                claim_uuid, created_at, updated_at, type, severity, status, description, photo_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            claim.claim_uuid,
            now,
            now,
            claim.type.value,
            claim.severity.value,
            Status.OPEN.value,
            claim.description,
            photo_path
        ))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        # Check if it exists to confirm it's a duplicate UUID
        existing = get_claim_by_uuid(claim.claim_uuid)
        if existing:
            raise DuplicateClaimError(f"Claim with UUID {claim.claim_uuid} already exists")
        raise
    finally:
        conn.close()

def get_claim(claim_id: int) -> Optional[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM claims WHERE id = ?", (claim_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Claim(**dict(row))
    return None

def get_claim_by_uuid(claim_uuid: str) -> Optional[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM claims WHERE claim_uuid = ?", (claim_uuid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Claim(**dict(row))
    return None

def list_claims(
    status: Optional[Status] = None,
    severity: Optional[str] = None,
    claim_type: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None
) -> List[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM claims WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status.value)
    if severity:
        query += " AND severity = ?"
        val = severity.value if hasattr(severity, "value") else severity
        params.append(val)
    if claim_type:
        query += " AND type = ?"
        val = claim_type.value if hasattr(claim_type, "value") else claim_type
        params.append(val)
    if search:
        query += " AND (description LIKE ? OR resolved_note LIKE ?)"
        search_term = f"%{search}%"
        params.extend([search_term, search_term])
    if date_from:
        query += " AND created_at >= ?"
        params.append(date_from)
    if date_to:
        query += " AND created_at <= ?"
        params.append(date_to)
        
    query += " ORDER BY created_at DESC, id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [Claim(**dict(row)) for row in rows]

def update_claim(claim_id: int, update: ClaimUpdate) -> Optional[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if update.description is not None:
        updates.append("description = ?")
        params.append(update.description)
    if update.severity is not None:
        updates.append("severity = ?")
        params.append(update.severity.value)
        
    if not updates:
        conn.close()
        return get_claim(claim_id)
        
    updates.append("updated_at = ?")
    params.append(datetime.now())
    
    params.append(claim_id)
    
    query = f"UPDATE claims SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
    return get_claim(claim_id)

def update_claim_status(claim_id: int, update: ClaimStatusUpdate) -> Optional[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    updates = ["status = ?", "updated_at = ?"]
    params = [update.status.value, now]
    
    # Handle resolved_at logic
    if update.status == Status.RESOLVED:
        updates.append("resolved_at = ?")
        params.append(now)
        if update.resolution_outcome:
            updates.append("resolution_outcome = ?")
            params.append(update.resolution_outcome.value)
    else:
        # If moving out of resolved, clear resolved_at
        updates.append("resolved_at = NULL")
        updates.append("resolution_outcome = NULL")
        
    if update.resolved_note is not None:
        updates.append("resolved_note = ?")
        params.append(update.resolved_note)
        
    params.append(claim_id)
    
    query = f"UPDATE claims SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
    return get_claim(claim_id)

def update_claim_photo(claim_id: int, photo_path: str) -> Optional[Claim]:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE claims 
        SET photo_path = ?, updated_at = ? 
        WHERE id = ?
    """, (photo_path, datetime.now(), claim_id))
    
    conn.commit()
    conn.close()
    
    return get_claim(claim_id)
