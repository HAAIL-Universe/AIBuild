from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from claims.db import init_db
from claims.models import ClaimType, Severity, Status, ClaimCreate, ClaimUpdate, ClaimStatusUpdate, ResolutionOutcome
from claims import repo, storage, export
import logging
import os
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging
logger = logging.getLogger("claims_tracker")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.FileHandler(storage.get_data_dir() / "app.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Basic Auth Logic
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = os.getenv("BASIC_AUTH_USER")
    correct_pass = os.getenv("BASIC_AUTH_PASS")
    
    if not correct_user or not correct_pass:
        return "auth_disabled"

    is_correct_user = secrets.compare_digest(credentials.username, correct_user)
    is_correct_pass = secrets.compare_digest(credentials.password, correct_pass)

    if not (is_correct_user and is_correct_pass):
        raise StarletteHTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Conditional Dependency
# We only enforce auth if env vars are set.
# We apply this to the FastAPI app, but exclude static mounts by nature of FastAPI dependencies.
app_dependencies = []
if os.getenv("BASIC_AUTH_USER") and os.getenv("BASIC_AUTH_PASS"):
    app_dependencies.append(Depends(get_current_username))
    logger.info("Basic Auth ENABLED")
else:
    logger.info("Basic Auth disabled")

app = FastAPI(title="Micro-Claims Tracker", dependencies=app_dependencies)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory=storage.get_data_dir() / "uploads"), name="uploads")

# Templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    status: Optional[Status] = None,
    severity: Optional[Severity] = None,
    type: Optional[ClaimType] = None,
    search: Optional[str] = None,
    range_preset: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    d_from = None
    d_to = None
    
    if range_preset == "week":
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        d_from = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_from:
        try:
            d_from = datetime.fromisoformat(date_from)
        except ValueError:
            pass
            
    if date_to:
        try:
            d_to = datetime.fromisoformat(date_to).replace(hour=23, minute=59, second=59)
        except ValueError:
            pass
        
    claims = repo.list_claims(
        status=status,
        severity=severity,
        claim_type=type,
        search=search,
        date_from=d_from,
        date_to=d_to
    )
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "claims": claims,
        "statuses": Status,
        "severities": Severity,
        "types": ClaimType,
        "filters": {
            "status": status,
            "severity": severity,
            "type": type,
            "search": search,
            "range_preset": range_preset,
            "date_from": date_from,
            "date_to": date_to
        },
        "data_dir": storage.get_data_dir()
    })

@app.get("/claims/new", response_class=HTMLResponse)
async def new_claim(request: Request):
    return templates.TemplateResponse("new_claim.html", {
        "request": request,
        "types": ClaimType,
        "severities": Severity,
        "data_dir": storage.get_data_dir()
    })

@app.post("/claims")
async def create_claim(
    claim_uuid: str = Form(...),
    type: ClaimType = Form(...),
    severity: Severity = Form(...),
    description: str = Form(...),
    photo: Optional[UploadFile] = File(None)
):
    if photo and photo.filename:
        # Enforce 5MB limit
        content = await photo.read()
        if len(content) > 5 * 1024 * 1024:
            logger.warning(f"Upload too large for claim {claim_uuid}")
            raise HTTPException(status_code=413, detail="File too large (max 5MB)")
        await photo.seek(0)

    try:
        claim_data = ClaimCreate(
            claim_uuid=claim_uuid,
            type=type,
            severity=severity,
            description=description
        )
        
        photo_path = None
        if photo and photo.filename:
            photo_path = storage.save_upload(photo, claim_uuid)
            
        claim_id = repo.create_claim(claim_data, photo_path)
        logger.info(f"Claim created: {claim_id} (UUID: {claim_uuid})")
        return RedirectResponse(url=f"/claims/{claim_id}", status_code=303)
        
    except repo.DuplicateClaimError:
        logger.warning(f"Duplicate claim attempt: {claim_uuid}")
        # Safe "already captured" behavior
        existing = repo.get_claim_by_uuid(claim_uuid)
        if existing:
            return RedirectResponse(url=f"/claims/{existing.id}", status_code=303)
        raise HTTPException(status_code=500, detail="Duplicate error but claim not found")

@app.get("/claims/{claim_id}", response_class=HTMLResponse)
async def claim_detail(request: Request, claim_id: int):
    claim = repo.get_claim(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
        
    return templates.TemplateResponse("claim_detail.html", {
        "request": request,
        "claim": claim,
        "severities": Severity,
        "statuses": Status,
        "outcomes": ResolutionOutcome,
        "data_dir": storage.get_data_dir()
    })

@app.post("/claims/{claim_id}/update")
async def update_claim(
    claim_id: int,
    description: Optional[str] = Form(None),
    severity: Optional[Severity] = Form(None),
    photo: Optional[UploadFile] = File(None)
):
    if photo and photo.filename:
        # Enforce 5MB limit
        content = await photo.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 5MB)")
        await photo.seek(0)

    if description is not None or severity is not None:
        repo.update_claim(claim_id, ClaimUpdate(description=description, severity=severity))
        
    if photo and photo.filename:
        claim = repo.get_claim(claim_id)
        if claim:
            new_photo_path = storage.save_upload(photo, claim.claim_uuid)
            
            # Delete old photo if it exists and is different (e.g. different extension)
            if claim.photo_path and claim.photo_path != new_photo_path:
                storage.delete_upload(claim.photo_path)
                
            repo.update_claim_photo(claim_id, new_photo_path)
            logger.info(f"Claim {claim_id} photo updated")
            
    return RedirectResponse(url=f"/claims/{claim_id}", status_code=303)

@app.post("/claims/{claim_id}/status")
async def update_status(
    claim_id: int,
    status: Status = Form(...),
    resolved_note: Optional[str] = Form(None),
    resolution_outcome: Optional[ResolutionOutcome] = Form(None)
):
    repo.update_claim_status(claim_id, ClaimStatusUpdate(
        status=status,
        resolved_note=resolved_note,
        resolution_outcome=resolution_outcome
    ))
    logger.info(f"Claim {claim_id} status updated to {status.value}")
    return RedirectResponse(url=f"/claims/{claim_id}", status_code=303)

@app.post("/export")
async def export_claims(
    date_from: str = Form(...),
    date_to: str = Form(...)
):
    try:
        d_from = datetime.fromisoformat(date_from)
        d_to = datetime.fromisoformat(date_to).replace(hour=23, minute=59, second=59)
        
        claims = repo.list_claims(date_from=d_from, date_to=d_to)
        digest = export.generate_digest(claims, d_from, d_to)
        
        filename = f"claims_digest_{d_from.date()}_to_{d_to.date()}.md"
        logger.info(f"Export generated for range {d_from.date()} to {d_to.date()}")
        
        return PlainTextResponse(
            digest,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except ValueError:
        logger.error("Export failed: Invalid date format")
        raise HTTPException(status_code=400, detail="Invalid date format")
