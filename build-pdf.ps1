# Labellift — genereer alle PDF's uit pdf-bron/*.html via Edge (headless).
# Gebruik:  powershell -ExecutionPolicy Bypass -File .\build-pdf.ps1
# Optioneel 1 hoofdstuk:  .\build-pdf.ps1 -Only dak

param([string]$Only = "")

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src  = Join-Path $here "pdf-bron"
$out  = Join-Path $here "pdf"
New-Item -ItemType Directory -Force -Path $out | Out-Null

$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "C:\Program Files\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path $edge)) { Write-Error "Microsoft Edge niet gevonden."; exit 1 }

$profile = Join-Path $env:TEMP "ll-edge-pdf"
$files = Get-ChildItem $src -Filter *.html
if ($Only) { $files = $files | Where-Object { $_.BaseName -eq $Only } }

foreach ($f in $files) {
  $pdf = Join-Path $out ($f.BaseName + ".pdf")
  $uri = ([System.Uri]$f.FullName).AbsoluteUri
  Write-Host "PDF: $($f.Name)  ->  pdf\$($f.BaseName).pdf"
  & $edge --headless=new --disable-gpu --no-pdf-header-footer --no-first-run `
    --virtual-time-budget=5000 "--user-data-dir=$profile" "--print-to-pdf=$pdf" $uri | Out-Null
}
Write-Host "Klaar. PDF's staan in: $out"
