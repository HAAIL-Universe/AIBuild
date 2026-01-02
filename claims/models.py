from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ClaimType(str, Enum):
    DAMAGE = "Damage"
    SHORTAGE = "Shortage"
    MISSING_KIT = "Missing Kit"
    SAFETY = "Safety"
    OTHER = "Other"

class Severity(str, Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"

class Status(str, Enum):
    OPEN = "Open"
    IN_REVIEW = "In Review"
    RESOLVED = "Resolved"

class ResolutionOutcome(str, Enum):
    VALID = "Valid"
    INVALID = "Invalid"

class ClaimBase(BaseModel):
    claim_uuid: str
    type: ClaimType
    severity: Severity
    description: str

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    description: Optional[str] = None
    severity: Optional[Severity] = None

class ClaimStatusUpdate(BaseModel):
    status: Status
    resolved_note: Optional[str] = None
    resolution_outcome: Optional[ResolutionOutcome] = None

class Claim(ClaimBase):
    id: int
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    status: Status
    resolved_note: Optional[str] = None
    resolution_outcome: Optional[ResolutionOutcome] = None
    photo_path: Optional[str] = None

    class Config:
        from_attributes = True
