# Executor Contract (Contract Read Gate)

This repo is built under a Director ↔ Executor relay workflow.

## Governance precedence
If multiple governance docs conflict, precedence is:
1) `contracts/EXECUTOR_CONTRACT.md`
2) `build_docs/directive.md` (project directive)
3) any `runbooks/*` (if present)
If still ambiguous: STOP with CONTRACT_CONFLICT.

## Non-negotiables
- Evidence before action. No “fix first, verify later”.
- Minimal diff only. No refactors unless explicitly requested.
- Respect diff budget; stop before exceeding.
- If a directive does not specify a diff budget (max files + max LOC), STOP with AMBIGUOUS_INTENT.

## Required stop reason enum (choose exactly one)
EVIDENCE_MISSING | AMBIGUOUS_INTENT | CONTRACT_CONFLICT | RISK_EXCEEDS_SCOPE | NON_DETERMINISTIC_BEHAVIOR | ENVIRONMENT_LIMITATION

## Evidence bundle (pre-action)
- Exact repro steps
- Console: first error or “none”
- Network: relevant request rows (name, status, response preview)
- UI/DOM/state proof when relevant
- Storage/DB proof when relevant

## Verification hierarchy (must report in order)
1) Static correctness
2) Runtime sanity
3) Behavioral intent
4) Contract compliance

## Post-execution reflection (non-actionable)
- 2–6 lines on fragility/ambiguity/over-constraint.
- No proposals, no next steps, no “could improve”.

## Output format
- Evidence bundle
- Classification
- Root-cause anchors (file:line)
- Patch summary
- Verification results (ordered)
- Reflection (non-actionable)
