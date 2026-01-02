import sqlite3
import os
from pathlib import Path
from .storage import get_data_dir

DB_NAME = "claims.db"

def get_db_path():
    return get_data_dir() / DB_NAME

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_uuid TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP NOT NULL,
        updated_at TIMESTAMP NOT NULL,
        resolved_at TIMESTAMP,
        type TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        description TEXT NOT NULL,
        resolved_note TEXT,
        resolution_outcome TEXT,
        photo_path TEXT
    )
    """)
    
    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_created_at ON claims(created_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_severity ON claims(severity)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_type ON claims(type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_claims_resolved_at ON claims(resolved_at)")

    # Migration Guard
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]
    if version == 0:
        cursor.execute("PRAGMA user_version = 1")
    elif version > 1:
        import logging
        logging.getLogger("claims_tracker").warning(f"DB version {version} is higher than expected (1).")
    
    conn.commit()
    conn.close()

def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn
