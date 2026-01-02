from datetime import datetime
from typing import List
from .models import Claim, Status, Severity, ClaimType

def generate_digest(claims: List[Claim], date_from: datetime, date_to: datetime) -> str:
    now = datetime.now()
    
    # Counts
    total = len(claims)
    by_status = {s: 0 for s in Status}
    by_severity = {s: 0 for s in Severity}
    by_type = {t: 0 for t in ClaimType}
    
    for c in claims:
        by_status[c.status] += 1
        by_severity[c.severity] += 1
        by_type[c.type] += 1
        
    lines = []
    lines.append(f"# Micro-Claims Weekly Digest")
    lines.append(f"Generated: {now.date().isoformat()}")
    lines.append(f"Range: {date_from.date()} to {date_to.date()}")
    lines.append("")
    
    lines.append("## Summary")
    lines.append(f"- Total Claims: {total}")
    lines.append("- By Status:")
    for s in Status:
        lines.append(f"  - {s.value}: {by_status[s]}")
    lines.append("- By Severity:")
    for s in Severity:
        lines.append(f"  - {s.value}: {by_severity[s]}")
    lines.append("- By Type:")
    for t in ClaimType:
        lines.append(f"  - {t.value}: {by_type[t]}")
    lines.append("")
    
    lines.append("## Claims List")
    lines.append("| ID | Date | Type | Severity | Status | Description | Outcome |")
    lines.append("|---|---|---|---|---|---|---|")
    
    for c in claims:
        created_str = c.created_at.isoformat(timespec='minutes')
        desc = c.description.replace("\n", " ").replace("|", " ")
        outcome = c.resolution_outcome.value if c.resolution_outcome else ""
        if c.resolved_note:
            outcome += f" ({c.resolved_note})"
            
        lines.append(f"| {c.id} | {created_str} | {c.type.value} | {c.severity.value} | {c.status.value} | {desc} | {outcome} |")
        
    return "\n".join(lines)
