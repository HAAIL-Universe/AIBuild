# AI Build: Contract-First App Build Demo

**A demonstration of a governed AI build workflow:**
Human-picked pain point &rarr; AI Designer/Director spec/contracts &rarr; AI Executor build + verification.

---

## What This Is
This repository is a **workflow demonstration**. It showcases how AI agents can collaborate to build a specific, scoped application ("Micro-Claims Tracker") by following strict contracts and directives.

- **Role-Based**: Distinct roles for Design (Director) and Implementation (Executor).
- **Contract-Driven**: Build boundaries are defined by `contracts/` and `build_docs/` before code is written.
- **Verification-First**: The Executor must prove compliance with the contract via `verify_compliance.py`.

## What This Isn't
- **One-Prompt Autopilot**: This was not built by a single "make me an app" prompt. It was an iterative, governed process.
- **Production SaaS**: The resulting app is a **low-risk demo** (local-first, no auth) intended for testing the *build process*, not for public deployment.

---

## Showcase

*Screenshots of the Micro-Claims Tracker application.*

### Dashboard
![Dashboard View](assets/dashboard.png)
*The main dashboard showing active claims, filters, and status indicators.*

### New Claim Workflow
![New Claim Form](assets/new-claim.png)
*Simple, mobile-friendly form for capturing issues on the floor.*

### Claim Detail
![Claim Detail](assets/detail.png)
*Detailed view with photo evidence and resolution controls.*

### Weekly Digest
![Export Preview](assets/export.png)
*Deterministic markdown export for weekly reporting.*

*(Note: If screenshots are missing, please run the app locally and capture them to `docs/assets/`)*

---

## Try It Yourself

You can run this application locally or self-host it for your team.

- **[View Source Code on GitHub](../)**
- **[Read the Self-Hosting Guide](SELF_HOSTING.md)**

---

## Workflow Artifacts

Explore the documents that drove this build:

- **[Blueprint](../build_docs/blueprint.md)**: The high-level architectural vision.
- **[Manifesto](../build_docs/manifesto.md)**: The core philosophy of the build.
- **[Directive](../build_docs/directive.md)**: The specific instructions for the Executor.
- **[Executor Contract](../contracts/EXECUTOR_CONTRACT.md)**: The rules of engagement.
- **[Runbook: UI Boot](../contracts/RUNBOOK_UI_BOOT.md)**: The specific UI requirements.
