
# M0 Hardening Pack — Source Control & Sync

**Purpose:** Keep your development reliable across machines without syncing virtual environments or SQLite DBs.

## Recommended Workflow (Git-first)
1. Keep your project folder **anywhere you like** (Desktop is fine if not OneDrive).
2. Initialize Git and push to GitHub/DevOps.
3. Each machine creates its **own .venv** (never synced).
4. Database (`db.sqlite3`) is **ignored** by Git to avoid merge conflicts. Use fixtures later if you need seed data.

## OneDrive (if you insist)
- You may store **code** under OneDrive, but keep the **venv outside OneDrive** (e.g., `C:\venvs\clever-bee`).
- Update `.vscode/settings.json` to point to that interpreter path.
- Do **not** run the dev server on two machines at the same time to avoid DB sync/locking issues.

## Quick Commands
```powershell
# Initialize Git (run in your project root)
git init
git add .
git commit -m "Initial commit - M0 baseline"

# After creating an empty repo online, then:
git branch -M main
git remote add origin <YOUR_REPO_HTTPS_URL>
git push -u origin main
```
