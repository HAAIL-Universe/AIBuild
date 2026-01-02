# UI Boot Runbook (Minimal)

## Boot order (must prove each layer)
1) Static assets load (HTML/CSS/JS reachable; no 404s)
2) App initializes (no fatal console errors)
3) API connectivity (expected endpoints reachable; localhost ok)
4) State hydration (DB reads return expected rows)
5) Primary interaction works end-to-end

## Evidence required when UI breaks
- Repro steps (click path)
- Console first error (or none)
- Network rows for key endpoints (name/status/preview)
- Screenshot or DOM proof of the broken state
- Relevant storage snapshots (localStorage/sessionStorage/cookies) if applicable

## Hard rules
- No UI “cleanups” during a fix.
- Patch must be minimal and localized.
- Verify boot order again after patch.
