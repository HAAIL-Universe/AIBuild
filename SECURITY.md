# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Deployment Models

This application has **NO** built-in user management or role-based access control.

### Safe Deployment Models
1.  **Local-Only (Recommended)**: Run on a single PC (`localhost`). No network exposure.
2.  **Cloud Self-Host (Secured)**: Deploy to a private cloud account (e.g., Render, Railway) **ONLY** if you enable the built-in Basic Auth (see below) or put it behind a VPN/Auth Proxy.
3.  **Internal LAN (Trusted)**: Run on a trusted internal network. **Warning**: Anyone on the Wi-Fi can access/edit data.

### Prohibited Deployments
- **Public Internet**: Do not expose port 8000 to the world without authentication.
- **Sensitive Data**: Do not store PII, HIPAA, or financial data.

## Authentication
As of v1.3, optional **Basic Auth** is available.
- Enable by setting `BASIC_AUTH_USER` and `BASIC_AUTH_PASS` environment variables.
- This provides a single gatekeeper credential for the entire app.

## Reporting a Vulnerability
If you discover a security vulnerability, please open an issue in the repository.
