
# M0 Environment Pack

This pack helps you **prove** M0 readiness on Windows 11 + VS Code with a Python virtual environment.

## Contents
- `scripts/m0_env_probe.ps1` — Produces a timestamped `m0_reports/m0_env_report_*.txt` with Python/Git/Django versions, execution policy, OneDrive risk check, and PATH snapshot.
- `.vscode/settings.json` — Pins VS Code to use the local venv (`.venv\Scripts\python.exe`) and auto-activates it.

## Quick Start (M0-only)
1. Open your project folder in VS Code (e.g., `clever-bee`).
2. Open Terminal (**PowerShell**).
3. Ensure your venv is active: `.\.venv\Scripts\activate`
4. Run the probe:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\scripts\m0_env_probe.ps1
   ```
5. Open the generated report under `m0_reports/` and attach it in chat if requested.

## What Good Looks Like
- Python: 3.12+ (you have 3.13.x — ideal)
- Django: 5.1.x
- Git: Present and versioned
- ExecutionPolicy: `RemoteSigned` or `Bypass` (activation works is sufficient)
- No OneDrive path for the workspace (recommended to avoid sync conflicts)

> This pack is M0-scoped only. Do not infer M1 actions from it.
