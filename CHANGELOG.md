# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-02

### Added
- **Logging Hardening**: Named logger (`claims_tracker`) with handler deduplication to prevent duplicate logs on reload.
- **Determinism**: Enforced ISO date formatting in exports and deterministic ordering (ID secondary sort) for lists and exports.
- **Database Indexes**: Added SQLite indexes for `created_at`, `status`, `severity`, `type`, and `resolved_at` to improve query performance.
- **Migration Guard**: Added `user_version` PRAGMA check to warn on schema version mismatches.
- **Verification**: Enhanced `verify_compliance.py` to check for logging configuration, DB indexes, and determinism.
- **Hygiene**: Recursive removal of `__pycache__` and stricter `.gitignore` rules.

### Changed
- Updated `main.py` logging configuration.
- Updated `claims/export.py` to use `isoformat` for dates.

## [1.0.0] - 2026-01-01

### Added
- Initial MVP release.
- Core Claims Management (Create, List, Filter, Resolve).
- Evidence Upload (Photo support).
- Weekly Digest Export (Markdown).
- Local SQLite Database.
- Basic UI with Jinja2 templates.
