# Micro-Claims Tracker — Manifesto

## Why this exists
Small operational problems are “too small” to log, so they disappear. That invisibility compounds cost. This tool exists to make tiny issues unignorable without adding process pain.

## Principles (non-negotiable)
1) **Speed wins adoption**
   - If capture isn’t fast, the system dies.
2) **Trust is everything**
   - No duplicates, no ambiguous “weekly” logic, no hidden data.
3) **Local-first by default**
   - Works offline by being local; avoids compliance and auth overhead in MVP.
4) **Determinism over cleverness**
   - Same inputs should produce the same digest. No surprises.
5) **Minimal moving parts**
   - FastAPI + Jinja + SQLite. Minimal JS. No front-end build pipeline.
6) **Guardrails before polish**
   - Close common failure modes early (timestamps, de-dupe, backup visibility).
7) **Hard scope boundaries**
   - No integrations, no multi-user, no LAN mode, no packaging in MVP.

## MVP values
- Capture is frictionless
- Retrieval is fast
- Exports are consistent and shareable
- Data is clearly stored and easy to back up manually

## What we refuse to do in MVP
- Auth/RBAC, external services, analytics, “while we’re here” features, or anything that forces compliance/security work.
