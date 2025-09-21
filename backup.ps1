$ErrorActionPreference = "Stop"
$src = "db.sqlite3"
if (!(Test-Path $src)) { Write-Host "No db.sqlite3 found. Nothing to back up."; exit 0 }
$destDir = "backups"
New-Item -ItemType Directory -Force -Path $destDir | Out-Null
$stamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
Copy-Item $src (Join-Path $destDir ("db_" + $stamp + ".sqlite3"))
Write-Host "Backup created: $(Join-Path $destDir ("db_" + $stamp + ".sqlite3"))"
