<# 
M0 Environment Probe (Windows PowerShell)
Purpose: Collect and persist environment facts to validate M0 readiness.
Usage:
  .\.venv\Scripts\activate
  powershell -ExecutionPolicy Bypass -File .\scripts\m0_env_probe.ps1
#>

$ErrorActionPreference = "Stop"

# Ensure output folder
$OutDir = Join-Path -Path (Get-Location) -ChildPath "m0_reports"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$ReportPath = Join-Path $OutDir ("m0_env_report_" + $Timestamp + ".txt")

function W($t){ Add-Content -Path $ReportPath -Value $t }

W "=== M0 Environment Report ==="
W ("Timestamp: " + (Get-Date).ToString("u"))
W ("Workspace: " + (Get-Location).Path)
W ""

# Execution policy
try { $execPol = Get-ExecutionPolicy -Scope CurrentUser } catch { $execPol = "Unknown" }
W ("ExecutionPolicy(CurrentUser): " + $execPol)

# OneDrive risk check
$oneDrive = $env:OneDrive
$ws = (Get-Location).Path
$underOD = ($oneDrive -and $ws -like "$oneDrive*")
W ("OneDriveEnvPresent: " + ([bool]$oneDrive))
W ("WorkspaceUnderOneDrive: " + $underOD)
W ""

# General-purpose runner
function Run([string]$label, [string]$cmd, [string]$argumentList){
  W ("--- " + $label + " ---")
  try {
    $p = Start-Process -NoNewWindow `
                       -FilePath $cmd `
                       -ArgumentList $argumentList `
                       -RedirectStandardOutput "STDOUT.tmp" `
                       -RedirectStandardError  "STDERR.tmp" `
                       -PassThru -Wait
    if (Test-Path "STDOUT.tmp"){ W ((Get-Content "STDOUT.tmp") -join "`n"); Remove-Item STDOUT.tmp -Force }
    if (Test-Path "STDERR.tmp"){ $e = (Get-Content "STDERR.tmp") -join "`n"; if($e.Trim().Length -gt 0){ W ("[stderr] " + $e) }; Remove-Item STDERR.tmp -Force }
  } catch { W ("[error] " + $_.Exception.Message) }
  W ""
}

Run "python --version"            "python" "--version"
Run "pip --version"               "python" "-m pip --version"
Run "git --version"               "git"    "--version"
Run "VS Code version"             "code"   "--version"
Run "Django version"              "python" "-m django --version"
Run "Installed Pythons (py -0p)"  "py"     "-0p"

$pathParts = $env:Path -split ';' | Where-Object { $_ -ne "" }
W "PATH entries (first 15 shown):"
$pathParts | Select-Object -First 15 | ForEach-Object { W ("  " + $_) }
if ($pathParts.Count -gt 15) { W ("  ... (" + ($pathParts.Count - 15) + " more)") }

W ""
W "=== End of Report ==="

Write-Host ("Report written to: " + $ReportPath)
