# Uploads everything in this folder to GitHub. The website updates about a minute later.
# Usage: right-click > Run with PowerShell, or run .\publish.ps1 in this folder.
Set-Location $PSScriptRoot
foreach ($g in Get-ChildItem -Directory | Where-Object { $_.Name -match '^\d+$' }) {
    if (-not (Get-ChildItem $g.FullName -Force)) { New-Item -ItemType File (Join-Path $g.FullName '.gitkeep') | Out-Null }
}
git add -A
git commit -m "Update lessons $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push
Write-Host "Done. The site updates in about a minute."
