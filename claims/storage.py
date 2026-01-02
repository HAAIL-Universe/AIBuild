import os
import shutil
from pathlib import Path
from fastapi import UploadFile

def get_data_dir() -> Path:
    # Check for env override first (for cloud persistence)
    env_override = os.getenv('CLAIMS_DATA_DIR')
    if env_override:
        data_dir = Path(env_override)
    elif os.name == 'nt':
        # Windows: %APPDATA%\claims_tracker
        base_dir = Path(os.getenv('APPDATA'))
        data_dir = base_dir / ".claims_tracker"
    else:
        # Linux/Mac: ~/.claims_tracker
        base_dir = Path.home()
        data_dir = base_dir / ".claims_tracker"
    
    data_dir.mkdir(parents=True, exist_ok=True)
    
    uploads_dir = data_dir / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir

def save_upload(file: UploadFile, claim_uuid: str) -> str:
    data_dir = get_data_dir()
    uploads_dir = data_dir / "uploads"
    
    # Get extension
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[1]
    if not ext:
        ext = ".jpg" # Default fallback
        
    # Save as claim_uuid + ext
    saved_filename = f"{claim_uuid}{ext}"
    file_path = uploads_dir / saved_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return str(saved_filename)

def get_upload_path(filename: str) -> Path:
    return get_data_dir() / "uploads" / filename

def delete_upload(filename: str):
    try:
        path = get_upload_path(filename)
        if path.exists():
            os.remove(path)
    except OSError:
        pass # Non-fatal

