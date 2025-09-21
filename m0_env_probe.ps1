<# 
M0 Environment Probe (Windows PowerShell)
Purpose: Collect and persist environment facts to validate M0 readiness.
Usage in VS Code Terminal (PowerShell):
  .\.venv\Scripts\Activate
  powershell -ExecutionPolicy Bypass -File .\scripts\m0_env_probe.ps1
#>

$ErrorActionPreference = "Stop"

# Ensure output folder
$OutDir = Join-Path -Path (Get-Location) -ChildPath "m0_reports"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$ReportPath = Join-Path $OutDir ("m0_env_report_" + $Timestamp + ".txt")

# Helper to append lines
function Append-Line($text) {
    Add-Content -Path $ReportPath -Value $text
}

Append-Line ("=== M0 Environment Report ===")
Append-Line ("Timestamp: " + (Get-Date).ToString("u"))
Append-Line ("Workspace: " + (Get-Location).Path)
Append-Line ""

# Execution policy (CurrentUser scope)
try {
    $execPol = Get-ExecutionPolicy -Scope CurrentUser
} catch {
    $execPol = "Unknown"
}
Append-Line ("ExecutionPolicy(CurrentUser): " + $execPol)

# OneDrive risk check
$oneDriveEnv = $env:OneDrive
$workspace = (Get-Location).Path
$oneDriveFlag = $false
if ($null -ne $oneDriveEnv) {
    if ($workspace -like "$oneDriveEnv*") {
        $oneDriveFlag = $true
    }
}
Append-Line ("OneDriveEnvPresent: " + ([bool]($null -ne $oneDriveEnv)))
Append-Line ("WorkspaceUnderOneDrive: " + $oneDriveFlag)

Append-Line ""

# Versions
function Safe-Run($label, $cmd, $args) {
    Append-Line ("--- " + $label + " ---")
    try {
        $p = Start-Process -NoNewWindow -FilePath $cmd -ArgumentList $args -RedirectStandardOutput "STDOUT.tmp" -RedirectStandardError "STDERR.tmp" -PassThru -Wait
        if (Test-Path "STDOUT.tmp") { Append-Line ((Get-Content "STDOUT.tmp") -join "`n") ; Remove-Item "STDOUT.tmp" -Force }
        if (Test-Path "STDERR.tmp") { $err = (Get-Content "STDERR.tmp") -join "`n"; if ($err.Trim().Length -gt 0) { Append-Line ("[stderr] " + $err) } ; Remove-Item "STDERR.tmp" -Force }
    } catch {
        Append-Line ("[error] " + $_.Exception.Message)
    }
    Append-Line ""
}

Safe-Run "python --version" "python" "--version"
Safe-Run "pip --version" "python" "-m pip --version"
Safe-Run "git --version" "git" "--version"
Safe-Run "VS Code version" "code" "--version"
Safe-Run "Django version" "python" "-m django --version"
Safe-Run "Installed Pythons (py -0p)" "py" "-0p"

# PATH snapshot (shortened for readability)
$pathParts = $env:Path -split ';' | Where-Object { $_ -ne "" }
Append-Line ("PATH entries (first 15 shown):")
$pathParts | Select-Object -First 15 | ForEach-Object { Append-Line ("  " + $_) }
if ($pathParts.Count -gt 15) { Append-Line ("  ... (" + ($pathParts.Count - 15) + " more)") }

Append-Line ""
Append-Line "=== End of Report ==="

Write-Host ("Report written to: " + $ReportPath)
